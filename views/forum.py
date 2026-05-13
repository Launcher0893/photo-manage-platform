from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, selectinload

from db import db
from models import ForumBoard, ForumComment, ForumPost, ForumPostImage, ForumPostLike
from utils.decorators import admin_required, user_required
from utils.file_upload import delete_uploaded_file, save_image_result
from utils.logger import log_admin_action


bp = Blueprint('forum', __name__, url_prefix='/forum')
admin_bp = Blueprint('admin_forum', __name__, url_prefix='/admin/forum')


@bp.route('/board')
def board():
    boards = db.session.execute(
        select(ForumBoard)
        .options(selectinload(ForumBoard.posts))
        .where(ForumBoard.status == 1)
        .order_by(ForumBoard.sort.asc(), ForumBoard.board_id.asc())
    ).scalars().all()
    return render_template('forum/board.html', boards=boards)


@bp.route('/post_list/<int:board_id>')
def post_list(board_id):
    page = request.args.get('page', default=1, type=int)
    keyword = request.args.get('keyword', '').strip()
    sort_by = request.args.get('sort_by', 'hot').strip().lower()
    board_item = db.session.get(ForumBoard, board_id)
    if board_item is None or board_item.status != 1:
        abort(404)

    hot_score = (
        func.coalesce(ForumPost.view_count, 0)
        + func.coalesce(ForumPost.like_count, 0) * 3
        + func.coalesce(ForumPost.comment_count, 0) * 2
    )
    stmt = (
        select(ForumPost)
        .options(joinedload(ForumPost.user))
        .where(ForumPost.board_id == board_id, ForumPost.status == 1)
    )
    if keyword:
        stmt = stmt.where(ForumPost.title.like(f'%{keyword}%'))
    if sort_by == 'new':
        stmt = stmt.order_by(ForumPost.is_top.desc(), ForumPost.create_time.desc(), ForumPost.post_id.desc())
    else:
        sort_by = 'hot'
        stmt = stmt.order_by(ForumPost.is_top.desc(), hot_score.desc(), ForumPost.create_time.desc(), ForumPost.post_id.desc())

    posts = db.paginate(stmt, page=page, per_page=10, error_out=False)
    return render_template('forum/post_list.html', board=board_item, posts=posts, keyword=keyword, sort_by=sort_by)


@bp.route('/post_detail/<int:post_id>')
def post_detail(post_id):
    post = db.session.execute(
        select(ForumPost)
        .options(
            joinedload(ForumPost.user),
            joinedload(ForumPost.forum_board),
            selectinload(ForumPost.images),
        )
        .where(ForumPost.post_id == post_id, ForumPost.status == 1)
    ).scalar_one_or_none()
    if post is None:
        abort(404)

    post.view_count = (post.view_count or 0) + 1
    db.session.commit()

    comments = db.session.execute(
        select(ForumComment)
        .options(joinedload(ForumComment.user))
        .where(ForumComment.post_id == post_id, ForumComment.status == 1)
        .order_by(ForumComment.create_time.asc(), ForumComment.comment_id.asc())
    ).scalars().all()
    is_liked = False
    if current_user.is_authenticated and not getattr(current_user, 'is_admin', False):
        is_liked = db.session.execute(
            select(ForumPostLike).where(
                ForumPostLike.post_id == post_id,
                ForumPostLike.user_id == current_user.user_id,
            )
        ).scalar_one_or_none() is not None
    return render_template('forum/post_detail.html', post=post, comments=comments, is_liked=is_liked)


@bp.route('/post_like/<int:post_id>', methods=['POST'])
def post_like(post_id):
    if not current_user.is_authenticated or getattr(current_user, 'is_admin', False):
        return jsonify({'success': False, 'message': '请先使用用户账号登录。'}), 401

    post = db.session.execute(
        select(ForumPost).where(
            ForumPost.post_id == post_id,
            ForumPost.status == 1,
        )
    ).scalar_one_or_none()
    if post is None:
        return jsonify({'success': False, 'message': '帖子不存在。'}), 404

    like = db.session.execute(
        select(ForumPostLike).where(
            ForumPostLike.post_id == post_id,
            ForumPostLike.user_id == current_user.user_id,
        )
    ).scalar_one_or_none()
    if like is None:
        db.session.add(ForumPostLike(post_id=post_id, user_id=current_user.user_id))
        liked = True
    else:
        db.session.delete(like)
        liked = False

    db.session.flush()
    post.like_count = db.session.scalar(
        select(func.count(ForumPostLike.like_id)).where(ForumPostLike.post_id == post_id)
    ) or 0
    db.session.commit()

    return jsonify({'success': True, 'liked': liked, 'count': post.like_count, 'message': '操作成功。'})


def _active_boards():
    return db.session.execute(
        select(ForumBoard)
        .where(ForumBoard.status == 1)
        .order_by(ForumBoard.sort.asc(), ForumBoard.board_id.asc())
    ).scalars().all()


@bp.route('/post_add', methods=['GET', 'POST'])
@bp.route('/post_add/<int:board_id>', methods=['GET', 'POST'])
@user_required
def post_add(board_id=None):
    boards = _active_boards()
    selected_board_id = board_id

    if request.method == 'POST':
        selected_board_id = request.form.get('board_id', type=int)
        board_item = db.session.get(ForumBoard, selected_board_id) if selected_board_id else None
        if board_item is None or board_item.status != 1:
            flash('请选择有效的论坛板块。', 'error')
            return render_template('forum/post_add.html', boards=boards, selected_board_id=selected_board_id)

        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not title or not content:
            flash('标题和内容不能为空。', 'error')
            return render_template('forum/post_add.html', boards=boards, selected_board_id=selected_board_id)

        post = ForumPost(
            board_id=selected_board_id,
            user_id=current_user.user_id,
            title=title,
            content=content,
            status=1,
        )
        db.session.add(post)
        db.session.flush()

        for sort, image_file in enumerate(request.files.getlist('post_images'), start=1):
            try:
                image_upload = save_image_result(image_file, 'forum')
            except ValueError as exc:
                db.session.rollback()
                flash(str(exc), 'error')
                return render_template('forum/post_add.html', boards=boards, selected_board_id=selected_board_id)
            if image_upload:
                db.session.add(
                    ForumPostImage(
                        post_id=post.post_id,
                        image_url=image_upload.url,
                        oss_object_name=image_upload.oss_object_name,
                        sort=sort,
                    )
                )

        db.session.commit()
        flash('帖子已发布。', 'success')
        return redirect(url_for('forum.post_detail', post_id=post.post_id))

    if selected_board_id is not None:
        board_item = db.session.get(ForumBoard, selected_board_id)
        if board_item is None or board_item.status != 1:
            abort(404)

    return render_template('forum/post_add.html', boards=boards, selected_board_id=selected_board_id)


@bp.route('/post_edit/<int:post_id>', methods=['GET', 'POST'])
@user_required
def post_edit(post_id):
    post = db.session.execute(
        select(ForumPost)
        .options(selectinload(ForumPost.images))
        .where(ForumPost.post_id == post_id, ForumPost.status == 1)
    ).scalar_one_or_none()
    if post is None:
        abort(404)
    if post.user_id != current_user.user_id:
        abort(403)

    boards = _active_boards()
    selected_board_id = post.board_id

    if request.method == 'POST':
        selected_board_id = request.form.get('board_id', type=int)
        board_item = db.session.get(ForumBoard, selected_board_id) if selected_board_id else None
        if board_item is None or board_item.status != 1:
            flash('请选择有效的论坛板块。', 'error')
            return render_template('forum/post_add.html', post=post, boards=boards, selected_board_id=selected_board_id)

        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not title or not content:
            flash('标题和内容不能为空。', 'error')
            return render_template('forum/post_add.html', post=post, boards=boards, selected_board_id=selected_board_id)

        delete_image_ids = {
            int(image_id)
            for image_id in request.form.getlist('delete_image_ids')
            if image_id.isdigit()
        }
        for image in list(post.images):
            if image.image_id in delete_image_ids:
                if not delete_uploaded_file(image.image_url, image.oss_object_name):
                    flash('图片文件删除失败，请稍后重试。', 'error')
                    return render_template('forum/post_add.html', post=post, boards=boards, selected_board_id=selected_board_id)
                db.session.delete(image)

        post.board_id = selected_board_id
        post.title = title
        post.content = content

        current_max_sort = max((image.sort or 0 for image in post.images), default=0)
        for offset, image_file in enumerate(request.files.getlist('post_images'), start=1):
            try:
                image_upload = save_image_result(image_file, 'forum')
            except ValueError as exc:
                db.session.rollback()
                flash(str(exc), 'error')
                return render_template('forum/post_add.html', post=post, boards=boards, selected_board_id=selected_board_id)
            if image_upload:
                db.session.add(
                    ForumPostImage(
                        post_id=post.post_id,
                        image_url=image_upload.url,
                        oss_object_name=image_upload.oss_object_name,
                        sort=current_max_sort + offset,
                    )
                )

        db.session.commit()
        flash('帖子已更新。', 'success')
        return redirect(url_for('forum.post_detail', post_id=post.post_id))

    return render_template('forum/post_add.html', post=post, boards=boards, selected_board_id=selected_board_id)


@bp.route('/comment_add/<int:post_id>', methods=['POST'])
@user_required
def comment_add(post_id):
    post = db.session.get(ForumPost, post_id)
    if post is None or post.status != 1:
        abort(404)
    content = request.form.get('content', '').strip()
    if not content:
        flash('评论内容不能为空。', 'error')
        return redirect(url_for('forum.post_detail', post_id=post_id))

    db.session.add(ForumComment(post_id=post_id, user_id=current_user.user_id, content=content, status=1))
    db.session.flush()
    post.comment_count = db.session.scalar(
        select(func.count(ForumComment.comment_id)).where(
            ForumComment.post_id == post_id,
            ForumComment.status == 1,
        )
    ) or 0
    db.session.commit()
    flash('评论已发布。', 'success')
    return redirect(url_for('forum.post_detail', post_id=post_id))


@admin_bp.route('/post_list')
@admin_required
def admin_post_list():
    page = request.args.get('page', default=1, type=int)
    title = request.args.get('title', '').strip()
    status = request.args.get('status', type=int)
    stmt = (
        select(ForumPost)
        .options(joinedload(ForumPost.user), joinedload(ForumPost.forum_board))
        .order_by(ForumPost.create_time.desc(), ForumPost.post_id.desc())
    )
    if title:
        stmt = stmt.where(ForumPost.title.like(f'%{title}%'))
    if status in (0, 1):
        stmt = stmt.where(ForumPost.status == status)
    posts = db.paginate(stmt, page=page, per_page=10, error_out=False)
    return render_template('forum/admin_post_list.html', posts=posts)


@admin_bp.route('/board_list')
@admin_required
def admin_board_list():
    page = request.args.get('page', default=1, type=int)
    board_name = request.args.get('board_name', '').strip()
    stmt = select(ForumBoard).order_by(ForumBoard.sort.asc(), ForumBoard.board_id.asc())
    if board_name:
        stmt = stmt.where(ForumBoard.board_name.like(f'%{board_name}%'))
    boards = db.paginate(stmt, page=page, per_page=10, error_out=False)
    return render_template('forum/admin_board_list.html', boards=boards)


@admin_bp.route('/board/add', methods=['GET', 'POST'])
@admin_bp.route('/board/edit/<int:board_id>', methods=['GET', 'POST'])
@admin_required
def admin_board_form(board_id=None):
    board_item = db.session.get(ForumBoard, board_id) if board_id else ForumBoard(status=1)
    if board_item is None:
        flash('论坛板块不存在。', 'error')
        return redirect(url_for('admin_forum.admin_board_list'))

    if request.method == 'POST':
        board_item.board_name = request.form.get('board_name', '').strip()
        board_item.description = request.form.get('description', '').strip() or None
        board_item.sort = request.form.get('sort', type=int, default=0)
        if not board_item.board_name:
            flash('板块名称不能为空。', 'error')
            return render_template('forum/admin_board_form.html', board=board_item)

        db.session.add(board_item)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('板块名称已存在。', 'error')
            return render_template('forum/admin_board_form.html', board=board_item)

        log_admin_action('论坛板块保存', f'保存论坛板块：{board_item.board_name}')
        flash('论坛板块已保存。', 'success')
        return redirect(url_for('admin_forum.admin_board_list'))

    return render_template('forum/admin_board_form.html', board=board_item if board_id else None)


@admin_bp.route('/board/status/<int:board_id>')
@admin_required
def toggle_board_status(board_id):
    board_item = db.session.get(ForumBoard, board_id)
    if board_item is not None:
        board_item.status = 0 if board_item.status == 1 else 1
        db.session.commit()
        log_admin_action('论坛板块状态', f'更新论坛板块状态：{board_item.board_name}')
        flash('论坛板块状态已更新。', 'success')
    return redirect(url_for('admin_forum.admin_board_list'))


@admin_bp.route('/comment_list')
@admin_required
def admin_comment_list():
    page = request.args.get('page', default=1, type=int)
    status = request.args.get('status', type=int)
    stmt = (
        select(ForumComment)
        .options(joinedload(ForumComment.user), joinedload(ForumComment.forum_post))
        .order_by(ForumComment.create_time.desc(), ForumComment.comment_id.desc())
    )
    if status in (0, 1):
        stmt = stmt.where(ForumComment.status == status)
    comments = db.paginate(stmt, page=page, per_page=10, error_out=False)
    return render_template('forum/admin_comment_list.html', comments=comments)


@admin_bp.route('/post/status/<int:post_id>')
@admin_bp.route('/post_delete/<int:post_id>')
@admin_required
def toggle_post_status(post_id):
    post = db.session.get(ForumPost, post_id)
    if post is not None:
        post.status = 0 if post.status == 1 else 1
        db.session.commit()
        log_admin_action('帖子状态', f'更新帖子状态：{post.title}')
        flash('帖子状态已更新。', 'success')
    return redirect(url_for('admin_forum.admin_post_list'))


@admin_bp.route('/post/top/<int:post_id>')
@admin_bp.route('/post_top/<int:post_id>')
@admin_required
def toggle_post_top(post_id):
    post = db.session.get(ForumPost, post_id)
    if post is not None:
        post.is_top = 0 if post.is_top == 1 else 1
        db.session.commit()
        log_admin_action('帖子置顶', f'更新帖子置顶：{post.title}')
        flash('帖子置顶状态已更新。', 'success')
    return redirect(url_for('admin_forum.admin_post_list'))


@admin_bp.route('/comment/status/<int:comment_id>')
@admin_bp.route('/comment_delete/<int:comment_id>')
@admin_required
def toggle_comment_status(comment_id):
    comment = db.session.get(ForumComment, comment_id)
    if comment is not None:
        comment.status = 0 if comment.status == 1 else 1
        post = db.session.get(ForumPost, comment.post_id)
        if post is not None:
            post.comment_count = db.session.scalar(
                select(func.count(ForumComment.comment_id)).where(
                    ForumComment.post_id == post.post_id,
                    ForumComment.status == 1,
                )
            ) or 0
        db.session.commit()
        log_admin_action('论坛评论状态', f'更新论坛评论：{comment.comment_id}')
        flash('评论状态已更新。', 'success')
    return redirect(url_for('admin_forum.admin_comment_list'))
