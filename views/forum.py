from flask import Blueprint, render_template

from utils.demo_data import Pagination, boards, get_board, get_post, posts


bp = Blueprint('forum', __name__, url_prefix='/forum')
admin_bp = Blueprint('admin_forum', __name__, url_prefix='/admin/forum')


@bp.route('/board')
def board():
    return render_template('forum/board.html', boards=boards)


@bp.route('/post_list/<int:board_id>')
def post_list(board_id):
    board = get_board(board_id) or boards[0]
    board_posts = [post for post in posts if post.forum_board.board_id == board.board_id]
    return render_template('forum/post_list.html', board=board, posts=Pagination(board_posts))


@bp.route('/post_detail/<int:post_id>')
def post_detail(post_id):
    post = get_post(post_id) or posts[0]
    post_comments = []
    return render_template('forum/post_detail.html', post=post, comments=post_comments)


@bp.route('/post_add/<int:board_id>', methods=['GET', 'POST'])
def post_add(board_id):
    board = get_board(board_id) or boards[0]
    return render_template('forum/post_add.html', board=board)


@admin_bp.route('/post_list')
def admin_post_list():
    return render_template('forum/admin_post_list.html', posts=Pagination(posts))


@admin_bp.route('/comment_list')
def admin_comment_list():
    return render_template('forum/admin_comment_list.html', comments=Pagination([]))
