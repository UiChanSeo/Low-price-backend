from flask import Blueprint, request
from flask import jsonify
from flask_login import login_required
from app.service.category_service import CategoryService

category_ctl = Blueprint('category_ctl', __name__, url_prefix='/category')


@category_ctl.route('/login/add/<title>', methods=['POST'])
@login_required
def add_category(title):
    print(__name__, 'add_category', title)
    CategoryService.add(title)

    return jsonify({"result": "Ok"})


def inc_category_count_internal(title: str):
    CategoryService.inc_cnt(title)
    return jsonify({"result": "Ok"})


def del_category_internal(title: str = None):
    print(__name__, 'del_category')
    CategoryService.delete(title)

    return jsonify({"result": "ok"})


@category_ctl.route('/login/del', methods=['POST'])
@login_required
def del_category_in_login():
    params = request.args.to_dict()
    if len(params) == 0 or 'title' not in params.keys():
        return del_category_internal()
    else:
        return del_category_internal(params['title'])


@category_ctl.route('/del', methods=['POST'])
def del_category(request_val):
    params = request_val.args.to_dict()
    if len(params) == 0 or 'title' not in params.keys():
        return del_category_internal()
    else:
        return del_category_internal(params['title'])


@category_ctl.route('/login/inc_count/<title>', methods=['POST'])
@login_required
def inc_category_count_in_login(title: str):
    return inc_category_count_internal(title)


@category_ctl.route('/inc_count/<title>', methods=['POST'])
def inc_category_count(title: str):
    return inc_category_count_internal(title)


@category_ctl.route('/test', methods=['GET'])
@login_required
def test_category(request_arg):
    return jsonify({"result": "Ok"})


def get_categories_internal(title: str = None):
    cas = CategoryService.get(title)
    categories = []
    for c in cas:
        categories.append(c.asdict())
    return jsonify({'len': len(cas), 'categories': categories})


@category_ctl.route('/get', methods=['GET'])
def get_categories():
    return get_categories_internal()


@category_ctl.route('/login/get', methods=['GET'])
@login_required
def get_categories_in_login():
    return get_categories_internal()
