from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload, selectinload

from db import db
from models import ForumBoard, ForumComment, ForumPost, ForumPostImage
from utils.decorators import admin_required, user_required
from utils.file_upload import save_image


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
    board_item = db.session.get(ForumBoard, board_id)
    if board_item is None or board_item.status != 1:
        abort(404)

    stmt = (
        select(ForumPost)
        .options(joinedload(ForumPost.user))
        .where(ForumPost.board_id == board_id, ForumPost.status == 1)
        .order_by(ForumPost.is_top.desc(), ForumPost.create_time.desc(), ForumPost.post_id.desc())
    )
    posts = db.paginate(stmt, page=page, per_page=10, error_out=False)
    return render_template('forum/post_list.html', board=board_item, posts=posts)


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
    return render_template('forum/post_detail.html', post=post, comments=comments)


@bp.route('/post_add/<int:board_id>', methods=['GET', 'POST'])
@user_required
def post_add(board_id):
    board_item = db.session.get(ForumBoard, board_id)
    if board_item is None or board_item.status != 1:
        abort(404)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not title or not content:
            flash('标题和内容不能为空。', 'error')
            return render_template('forum/post_add.html', board=board_item)

        post = ForumPost(
            board_id=board_id,
            user_id=current_user.user_id,
            title=title,
            content=content,
            status=1,
        )
        db.session.add(post)
        db.session.flush()

        for sort, image_file in enumerate(request.files.getlist('post_images'), start=1):
            try:
                image_url = save_image(image_file, 'forum')
            except ValueError as exc:
                db.session.rollback()
                flash(str(exc), 'error')
                return render_template('forum/post_add.html', board=board_item)
            if image_url:
                db.session.add(ForumPostImage(post_id=post.post_id, image_url=image_url, sort=sort))

        db.session.commit()
        flash('帖子已发布。', 'success')
        return redirect(url_for('forum.post_detail', post_id=post.post_id))

    return render_template('forum/post_add.html', board=board_item)


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
        flash('评论状态已更新。', 'success')
    return redirect(url_for('admin_forum.admin_comment_list'))
