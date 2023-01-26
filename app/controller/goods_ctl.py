from flask import Blueprint, request
from flask import jsonify
from flask_login import login_required
from app.model.goods import Goods
from app.service.goods_service import GoodsService


goods_ctl=Blueprint('goods_ctl', __name__, url_prefix='/goods')


@goods_ctl.route('/login/add', methods=['POST'])
@login_required
def add_goods_with_id():
    params = request.get_json(force=True)
    if params is not None:
        goods_name = params['name']
        category_id = params['category_id']
        goods_url = params['goods_url']
        image_url = params['image_url']
        mall_name = params['mall_name']
        lprice = params['lprice']
        hprice = params['hprice']
        GoodsService.add(
            Goods(
            name = goods_name,
            category_id = category_id,
            goods_url = goods_url,
            image_url = image_url,
            mall_name = mall_name,
            lprice = lprice,
            hprice = hprice,
            cnt = 1))
        return jsonify({"result":"ok"})
    return jsonify({"result":"fail"})


def get_goods_with_id_internal(request):
    params = request.args.to_dict()

    if len(params) == 0 or 'name' not in params.keys():
        return jsonify({"result":"false", "reson":"no parameter"})

    name = params['name']

    if 'category' in params.keys():
        category_id = int(params['category'])
    else:
        category_id = -1

    if 'limit' in params.keys():
        sel_limit = int(params['limit'])
    else:
        sel_limit = 20

    if name == '*':
        name = None
    cnt, goods_list = GoodsService.get(name = name,
                                       category_id = category_id,
                                       sel_limit = sel_limit)
    goods_dicts = []

    for goods in goods_list:
        goods_dicts.append(goods.asdict())

    return {"len":cnt, "goods":goods_dicts}


def del_goods_with_id_internal(request):

    params = request.args.to_dict()

    if len(params) == 0 or 'name' not in params.keys():
        return jsonify({"result":"false", "reson":"no parameter"})

    name = params['name']

    if 'mall_name' in params.keys():
        mall_name = params['mall_name']
    else:
        mall_name = None

    if 'category_id' in params.keys():
        category_id = int(params['category_id'])
    else:
        category_id = -1

    if name == '*':
        GoodsService.delete()
    else:
        GoodsService.delete(name=name,
                            category_id=category_id,
                            mall_name=mall_name)

    return jsonify({"result":"ok"})


@goods_ctl.route('/get/id', methods=['POST'])
def get_goods_with_id():
    return get_goods_with_id_internal(request)


@goods_ctl.route('/login/get/id', methods=['POST'])
@login_required
def get_goods_with_id_with_login():
    return get_goods_with_id_internal(request)


@goods_ctl.route('/del/id', methods=['POST'])
def del_goods_with_id():
    return del_goods_with_id_internal(request)


@goods_ctl.route('/login/del/id', methods=['POST'])
@login_required
def del_goods_with_id_with_login():
    return del_goods_with_id_internal(request)
