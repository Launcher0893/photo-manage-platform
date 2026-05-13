from flask import Blueprint, jsonify, request

from utils.demo_data import get_work


bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/work/<int:work_id>/like', methods=['POST'])
def like_work(work_id):
    work = get_work(work_id)
    count = work.like_count if work else 0
    return jsonify({'success': True, 'liked': True, 'count': count})


@bp.route('/work/<int:work_id>/comment', methods=['POST'])
def add_comment(work_id):
    _ = request.form.get('content', '')
    return jsonify({'success': True})
