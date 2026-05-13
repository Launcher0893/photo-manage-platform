from dataclasses import dataclass

from flask import Blueprint, render_template


@dataclass
class DemoCarousel:
    carousel_id: int
    title: str
    image_url: str
    link_type: str = ''
    link_id: int | None = None
    link_url: str = ''
    sort: int = 0
    status: int = 1


carousels = [
    DemoCarousel(1, '首页横幅', 'https://via.placeholder.com/300x120', 'work', 1, '', 1, 1),
]


bp = Blueprint('carousel', __name__, url_prefix='/admin/carousel')


@bp.route('/list')
def list_page():
    return render_template('carousel/list.html', carousels=carousels)


@bp.route('/add', methods=['GET', 'POST'])
@bp.route('/edit/<int:carousel_id>', methods=['GET', 'POST'])
def form(carousel_id=None):
    carousel = next((item for item in carousels if item.carousel_id == carousel_id), None)
    return render_template('carousel/form.html', carousel=carousel)
