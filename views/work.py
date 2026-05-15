"""作品模块。

前台蓝图前缀：/work
后台蓝图前缀：/admin/work

本文件负责：
- 前台作品列表和作品详情。
- 摄影师发布、编辑、上下架自己的作品。
- 管理员后台管理全部作品、审核作品、管理作品评论。

常见跳转关系：
- render_template('work/list.html') -> templates/work/list.html
- url_for('work.my_works') -> my_works() -> /work/my
- url_for('admin_work.admin_list') -> admin_list() -> /admin/work/list
"""

from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload, selectinload

from db import db
from models import Category, PhotoWork, PhotoWorkImage, Photographer, User, WorkComment, WorkLike
from utils.decorators import admin_required, user_required
from utils.file_upload import delete_uploaded_file, save_image_result
from utils.logger import log_admin_action


# bp 是前台作品蓝图，@bp.route('/list') 注册后完整地址是 /work/list。
bp = Blueprint('work', __name__, url_prefix='/work')

# admin_bp 是后台作品蓝图，@admin_bp.route('/list') 注册后完整地址是 /admin/work/list。
admin_bp = Blueprint('admin_work', __name__, url_prefix='/admin/work')


def _approved_current_photographer():
    """获取当前登录用户对应的“审核通过摄影师”记录。

    current_user 来自 Flask-Login。
    如果当前用户没有摄影师资料，或摄影师认证没通过，返回 None。
    """
    photographer = current_user.photographer
    if photographer is None or photographer.cert_status != Photographer.STATUS_APPROVED:
        return None
    return photographer


def _active_categories():
    """查询启用状态的作品分类，用于发布/编辑作品时的分类下拉框。"""
    return db.session.execute(
        select(Category).where(Category.status == 1).order_by(Category.sort.asc(), Category.category_id.asc())
    ).scalars().all()


def _append_missing_by_id(items, current_item, id_attr):
    """后台编辑时保留旧关联项。

    例如作品原来的分类现在被停用了，正常“启用分类列表”里查不到它。
    为了编辑页面还能显示原分类，需要把 current_item 补回列表。
    """
    if current_item is not None and all(getattr(item, id_attr) != getattr(current_item, id_attr) for item in items):
        return [current_item, *items]
    return items


def _save_work_from_request(
    work,
    categories,
    template_name,
    redirect_endpoint,
    log_operation=None,
    log_content_factory=None,
    **template_context,
):
    """保存作品表单的公共函数。

    摄影师前台发布/编辑作品和管理员后台新增/编辑作品都会调用它。
    它负责读取表单、保存封面、保存组图、删除旧图、更新热度、提交数据库。

    template_name：保存失败时回到哪个模板。
    redirect_endpoint：保存成功后跳到哪个 endpoint，例如 work.my_works 或 admin_work.admin_list。
    """
    old_cover_url = None

    # request.form 读取 HTML 表单提交的数据，name="title" 对应这里的 title。
    work.title = request.form.get('title', '').strip()
    work.category_id = request.form.get('category_id', type=int)
    work.city = request.form.get('city', '').strip() or None
    work.description = request.form.get('description', '').strip() or None

    if not work.title or not work.photographer_id or not work.category_id:
        flash('标题、摄影师和分类不能为空。', 'error')
        return render_template(template_name, work=work, categories=categories, **template_context)

    # 编辑作品时，页面会把勾选删除的旧图片 id 放到 delete_image_ids。
    delete_image_ids = {
        int(image_id)
        for image_id in request.form.getlist('delete_image_ids')
        if image_id.isdigit()
    }
    for image in list(getattr(work, 'images', []) or []):
        if image.image_id in delete_image_ids:
            if not delete_uploaded_file(image.image_url, image.oss_object_name):
                flash('作品图片删除失败，请稍后重试。', 'error')
                return render_template(template_name, work=work, categories=categories, **template_context)
            db.session.delete(image)

    try:
        # request.files 读取上传文件；save_image_result 会保存本地并上传 OSS。
        cover_upload = save_image_result(request.files.get('cover_file'), 'works')
        if cover_upload:
            old_cover_url = work.cover_url
            work.cover_url = cover_upload.url
    except ValueError as exc:
        flash(str(exc), 'error')
        return render_template(template_name, work=work, categories=categories, **template_context)

    # add 把对象交给数据库 session 管理；flush 会先执行 SQL，以便新作品拿到 work_id。
    db.session.add(work)
    db.session.flush()

    # 追加组图时从当前最大 sort 往后排，避免新旧图片顺序冲突。
    current_max_sort = max((image.sort or 0 for image in getattr(work, 'images', []) or []), default=0)
    for offset, image_file in enumerate(request.files.getlist('work_images'), start=1):
        try:
            image_upload = save_image_result(image_file, 'works')
        except ValueError as exc:
            db.session.rollback()
            flash(str(exc), 'error')
            return render_template(template_name, work=work, categories=categories, **template_context)
        if image_upload:
            db.session.add(
                PhotoWorkImage(
                    work_id=work.work_id,
                    image_url=image_upload.url,
                    oss_object_name=image_upload.oss_object_name,
                    sort=current_max_sort + offset,
                )
            )

    # 保存前重新计算热度，热度由浏览、点赞、评论数综合计算。
    work.update_hot_score()
    db.session.commit()
    delete_uploaded_file(old_cover_url)
    if log_operation:
        log_content = log_content_factory(work) if log_content_factory else work.title
        log_admin_action(log_operation, log_content)
    flash('作品已保存。', 'success')
    return redirect(url_for(redirect_endpoint))


@bp.route('/list')
def list_page():
    """作品列表页：完整访问地址 /work/list。

    从 URL 查询参数读取关键词、分类、城市、排序方式。
    只展示审核通过、已上架、摄影师账号正常的作品。
    最后把 works 和 categories 传给 templates/work/list.html。
    """
    page = request.args.get('page', default=1, type=int)
    keyword = request.args.get('keyword', '').strip()
    category_id = request.args.get('category_id', type=int)
    city = request.args.get('city', '').strip()
    sort_by = request.args.get('sort_by', 'hot').strip().lower()

    categories = db.session.execute(
        select(Category)
        .where(Category.status == 1)
        .order_by(Category.sort.asc(), Category.category_id.asc())
    ).scalars().all()

    # stmt 是还没执行的查询语句；后面会继续按筛选条件追加 where/order_by。
    stmt = (
        select(PhotoWork)
        .options(
            joinedload(PhotoWork.category),
            joinedload(PhotoWork.photographer).joinedload(Photographer.user),
        )
        # join 连接 photographer 和 user 表，这样才能过滤摄影师账号状态。
        .join(PhotoWork.photographer)
        .join(Photographer.user)
        .where(
            PhotoWork.audit_status == PhotoWork.AUDIT_APPROVED,
            PhotoWork.status == 1,
            User.status == 1,
        )
    )

    if keyword:
        stmt = stmt.where(PhotoWork.title.like(f'%{keyword}%'))
    if category_id:
        stmt = stmt.where(PhotoWork.category_id == category_id)
    if city:
        stmt = stmt.where(PhotoWork.city.like(f'%{city}%'))

    if sort_by == 'new':
        stmt = stmt.order_by(PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
    else:
        stmt = stmt.order_by(PhotoWork.hot_score.desc(), PhotoWork.create_time.desc(), PhotoWork.work_id.desc())

    # db.paginate 执行分页查询；works.items 是当前页作品，works.pages 是总页数。
    works = db.paginate(stmt, page=page, per_page=9, error_out=False)
    return render_template('work/list.html', works=works, categories=categories)


@bp.route('/my')
@user_required
def my_works():
    """我的作品页：完整访问地址 /work/my。

    @user_required 先保证访问者是已登录的普通用户/摄影师。
    函数内部再检查当前用户是否为审核通过的摄影师。
    """
    photographer = _approved_current_photographer()
    if photographer is None:
        flash('摄影师审核通过后才能管理作品。', 'error')
        return redirect(url_for('user.profile'))

    page = request.args.get('page', default=1, type=int)
    stmt = (
        select(PhotoWork)
        .options(joinedload(PhotoWork.category))
        .where(PhotoWork.photographer_id == photographer.photographer_id)
        .order_by(PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
    )
    works = db.paginate(stmt, page=page, per_page=10, error_out=False)
    return render_template('work/my_list.html', works=works)


@bp.route('/add', methods=['GET', 'POST'])
@bp.route('/edit/<int:work_id>', methods=['GET', 'POST'])
@user_required
def photographer_form(work_id=None):
    """摄影师发布/编辑作品。

    /work/add：work_id 为 None，表示新增作品。
    /work/edit/<work_id>：work_id 有值，表示编辑作品。
    GET 打开 templates/work/form.html；POST 提交表单并保存。
    """
    photographer = _approved_current_photographer()
    if photographer is None:
        flash('摄影师审核通过后才能发布作品。', 'error')
        return redirect(url_for('user.profile'))

    if work_id:
        # 编辑时同时限制 work_id 和 photographer_id，防止摄影师编辑别人的作品。
        work = db.session.execute(
            select(PhotoWork)
            .options(selectinload(PhotoWork.images))
            .where(
                PhotoWork.work_id == work_id,
                PhotoWork.photographer_id == photographer.photographer_id,
            )
        ).scalar_one_or_none()
        if work is None:
            abort(404)
    else:
        # 新作品默认上架且审核通过，这是当前课程项目设定。
        work = PhotoWork(
            photographer_id=photographer.photographer_id,
            status=1,
            audit_status=PhotoWork.AUDIT_APPROVED,
        )

    categories = _active_categories()
    if request.method == 'POST':
        work.photographer_id = photographer.photographer_id
        work.audit_status = PhotoWork.AUDIT_APPROVED
        return _save_work_from_request(work, categories, 'work/form.html', 'work.my_works')

    return render_template('work/form.html', work=work if work_id else None, categories=categories)


@bp.route('/status/<int:work_id>', methods=['POST'])
@user_required
def toggle_my_work_status(work_id):
    """摄影师下架/恢复自己的作品。

    POST /work/status/<work_id>
    status=1 表示上架，status=0 表示下架。
    """
    photographer = _approved_current_photographer()
    if photographer is None:
        flash('摄影师审核通过后才能管理作品。', 'error')
        return redirect(url_for('user.profile'))

    work = db.session.execute(
        select(PhotoWork).where(
            PhotoWork.work_id == work_id,
            PhotoWork.photographer_id == photographer.photographer_id,
        )
    ).scalar_one_or_none()
    if work is None:
        abort(404)

    work.status = 0 if work.status == 1 else 1
    db.session.commit()
    flash('作品状态已更新。', 'success')
    return redirect(url_for('work.my_works'))


@bp.route('/detail/<int:work_id>')
def detail(work_id):
    """作品详情页：完整访问地址 /work/detail/<work_id>。

    查询公开可见作品，进入详情页时增加浏览量并更新热度。
    同时查询评论列表和当前用户是否已点赞。
    """
    work = db.session.execute(
        select(PhotoWork)
        .options(
            joinedload(PhotoWork.category),
            joinedload(PhotoWork.photographer).joinedload(Photographer.user),
            selectinload(PhotoWork.images),
        )
        .join(PhotoWork.photographer)
        .join(Photographer.user)
        .where(
            PhotoWork.work_id == work_id,
            PhotoWork.audit_status == PhotoWork.AUDIT_APPROVED,
            PhotoWork.status == 1,
            User.status == 1,
        )
    ).scalar_one_or_none()

    if work is None:
        abort(404)

    # 用户进入详情页就增加一次浏览量。
    work.view_count = (work.view_count or 0) + 1
    work.update_hot_score()
    db.session.commit()

    comments = db.session.execute(
        select(WorkComment)
        .options(joinedload(WorkComment.user))
        .where(
            WorkComment.work_id == work_id,
            WorkComment.status == 1,
            WorkComment.audit_status == 1,
        )
        .order_by(WorkComment.create_time.asc(), WorkComment.comment_id.asc())
    ).scalars().all()

    is_liked = False
    if current_user.is_authenticated and not getattr(current_user, 'is_admin', False):
        is_liked = db.session.execute(
            select(WorkLike).where(
                WorkLike.work_id == work_id,
                WorkLike.user_id == current_user.user_id,
            )
        ).scalar_one_or_none() is not None

    return render_template('work/detail.html', work=work, comments=comments, is_liked=is_liked)


@admin_bp.route('/list')
@admin_required
def admin_list():
    """后台作品管理列表：完整访问地址 /admin/work/list。

    管理员可按标题、审核状态、上下架状态、是否精选筛选作品。
    """
    page = request.args.get('page', default=1, type=int)
    title = request.args.get('title', '').strip()
    audit_status = request.args.get('audit_status', type=int)
    status = request.args.get('status', type=int)
    is_featured = request.args.get('is_featured', type=int)

    stmt = (
        select(PhotoWork)
        .options(
            joinedload(PhotoWork.category),
            joinedload(PhotoWork.photographer).joinedload(Photographer.user),
        )
        .order_by(PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
    )
    if title:
        stmt = stmt.where(PhotoWork.title.like(f'%{title}%'))
    if audit_status in (0, 1, 2):
        stmt = stmt.where(PhotoWork.audit_status == audit_status)
    if status in (0, 1):
        stmt = stmt.where(PhotoWork.status == status)
    if is_featured in (0, 1):
        stmt = stmt.where(PhotoWork.is_featured == is_featured)

    works = db.paginate(stmt, page=page, per_page=10, error_out=False)
    return render_template('work/admin_list.html', works=works)


@admin_bp.route('/add', methods=['GET', 'POST'])
@admin_bp.route('/edit/<int:work_id>', methods=['GET', 'POST'])
@admin_required
def admin_form(work_id=None):
    """后台新增/编辑作品。

    与摄影师前台不同，管理员可以选择摄影师，也可以设置首页精选 is_featured。
    保存仍复用 _save_work_from_request()。
    """
    work = (
        db.session.execute(
            select(PhotoWork)
            .options(
                joinedload(PhotoWork.photographer).joinedload(Photographer.user),
                joinedload(PhotoWork.category),
                selectinload(PhotoWork.images),
            )
            .where(PhotoWork.work_id == work_id)
        ).scalar_one_or_none()
        if work_id
        else PhotoWork(status=1, audit_status=PhotoWork.AUDIT_APPROVED)
    )
    if work is None:
        flash('作品不存在。', 'error')
        return redirect(url_for('admin_work.admin_list'))

    photographers = db.session.execute(
        select(Photographer)
        .options(joinedload(Photographer.user))
        .where(Photographer.cert_status == Photographer.STATUS_APPROVED)
        .order_by(Photographer.photographer_id.desc())
    ).scalars().all()
    categories = _active_categories()
    photographers = _append_missing_by_id(photographers, getattr(work, 'photographer', None), 'photographer_id')
    categories = _append_missing_by_id(categories, getattr(work, 'category', None), 'category_id')

    if request.method == 'POST':
        work.photographer_id = request.form.get('photographer_id', type=int)
        work.is_featured = 1 if request.form.get('is_featured') == '1' else 0
        response = _save_work_from_request(
            work,
            categories,
            'work/admin_form.html',
            'admin_work.admin_list',
            log_operation='作品保存',
            log_content_factory=lambda saved_work: f'保存作品：{saved_work.title}',
            photographers=photographers,
        )
        return response

    return render_template(
        'work/admin_form.html',
        work=work if work_id else None,
        photographers=photographers,
        categories=categories,
    )


@admin_bp.route('/<int:work_id>/audit', methods=['POST'])
@admin_required
def audit(work_id):
    """后台作品审核接口。

    POST /admin/work/<work_id>/audit
    返回 JSON，通常由后台页面 Ajax 调用。
    """
    work = db.session.get(PhotoWork, work_id)
    if work is None:
        return jsonify({'success': False, 'message': '作品不存在。'}), 404
    audit_status = request.form.get('audit_status', type=int)
    if audit_status not in (PhotoWork.AUDIT_APPROVED, PhotoWork.AUDIT_REJECTED):
        return jsonify({'success': False, 'message': '审核状态无效。'}), 400
    work.audit_status = audit_status
    db.session.commit()
    log_admin_action('作品审核', f'审核作品：{work.title}')
    return jsonify({'success': True})


@admin_bp.route('/delete/<int:work_id>', methods=['POST'])
@admin_bp.route('/status/<int:work_id>', methods=['POST'])
@admin_required
def toggle_status(work_id):
    """后台下架/恢复作品。

    delete 和 status 两个地址都指向同一逻辑，用于兼容不同模板里的旧链接。
    """
    work = db.session.get(PhotoWork, work_id)
    if work is not None:
        work.status = 0 if work.status == 1 else 1
        db.session.commit()
        action = '下架' if work.status == 0 else '恢复'
        log_admin_action('作品状态', f'{action}作品：{work.title}')
        flash(f'作品已{action}。', 'success')
    return redirect(url_for('admin_work.admin_list'))


delete = toggle_status


@admin_bp.route('/comment_list')
@admin_required
def comment_list():
    """后台作品评论列表：完整访问地址 /admin/work/comment_list。"""
    page = request.args.get('page', default=1, type=int)
    status = request.args.get('status', type=int)
    audit_status = request.args.get('audit_status', type=int)

    stmt = (
        select(WorkComment)
        .options(joinedload(WorkComment.user), joinedload(WorkComment.photo_work))
        .order_by(WorkComment.create_time.desc(), WorkComment.comment_id.desc())
    )
    if status in (0, 1):
        stmt = stmt.where(WorkComment.status == status)
    if audit_status in (0, 1, 2):
        stmt = stmt.where(WorkComment.audit_status == audit_status)

    comments = db.paginate(stmt, page=page, per_page=10, error_out=False)
    return render_template('work/admin_comment_list.html', comments=comments)


@admin_bp.route('/comment/status/<int:comment_id>', methods=['POST'])
@admin_required
def toggle_comment_status(comment_id):
    """后台隐藏/恢复作品评论，并同步更新作品评论数和热度。"""
    comment = db.session.get(WorkComment, comment_id)
    if comment is not None:
        comment.status = 0 if comment.status == 1 else 1
        work = db.session.get(PhotoWork, comment.work_id)
        if work is not None:
            work.comment_count = db.session.scalar(
                select(func.count(WorkComment.comment_id)).where(
                    WorkComment.work_id == work.work_id,
                    WorkComment.status == 1,
                    WorkComment.audit_status == 1,
                )
            ) or 0
            work.update_hot_score()
        db.session.commit()
        log_admin_action('作品评论状态', f'更新作品评论：{comment.comment_id}')
        flash('作品评论状态已更新。', 'success')
    return redirect(url_for('admin_work.comment_list'))
