import datetime
import json
import logging
import time

from flask import request, jsonify, render_template
from pyecharts import Page, Bar
from sqlalchemy import func

from app.apps import db
from app.interface import inter
from app.models import GoodsType, TypeItem, Order, OrderDetail, Guest
from app.src.compute import user_statistics, compute_order_statistics
from app.utils.base_res import base_success_res, base_fail_res
from app.utils.doc import admin_login_req


@inter.route("/add_order", methods=['POST'])
# @admin_login_req
def add_order():
    try:
        request_data = request.get_data().decode('utf-8')
        request_json = json.loads(request_data)
        order_id = request_json.get("id")
        if not order_id:
            order = Order(
                order_no=time.strftime("%y%m%d%H%M%s", time.localtime()),
                guest_id=request_json.get("guest_id"),
                total=request_json.get("total"),
                pay=request_json.get("pay"),
                unpay=request_json.get("unpay"),
                description=request_json.get("description"),
                operator_id=request_json.get("admin_id")
            )
            db.session.add(order)
            if request_json.get('details'):
                for item in request_json.get('details'):
                    detail = {}
                    detail['type_id'] = item.pop('type_id')
                    detail['item_id'] = item.pop('item_id')
                    detail['price'] = item.pop('price')
                    detail['num'] = item.pop('num')
                    detail['status'] = 1
                    detail['lengh'] = item.pop('length')
                    new_item = OrderDetail(**detail)
                    order.order_detail.append(new_item)
            db.session.commit()
        else:
            db.session.query(Order).filter(Order.id == order_id).update({
                Order.guest_id: request_json.get('guest_id'),
                Order.total: request_json.get('total'),
                Order.pay: request_json.get('pay'),
                Order.unpay: request_json.get('unpay'),
                Order.description: request_json.get('description')
            })

            order_base = db.session.query(Order, Guest) \
                .join(Guest, Order.guest_id == Guest.user_id) \
                .filter(Order.id == order_id).first()
            if not order_base:
                return jsonify(base_fail_res("订单号", {"items": []}))
            origin_details = db.session.query(OrderDetail.id) \
                .join(GoodsType, GoodsType.id == OrderDetail.type_id) \
                .join(TypeItem, TypeItem.id == OrderDetail.item_id) \
                .filter(order_base[0].id == OrderDetail.order_id, OrderDetail.status == 1).all()
            new_details = request_json.get('details')

            if not origin_details and not new_details:
                db.session.commit()
            elif not origin_details and new_details:
                # add
                objs = list()
                for _ in new_details:
                    o = OrderDetail(
                        order_id=order_id,
                        type_id=_.get('type_id'),
                        item_id=_.get('item_id'),
                        price=_.get('price'),
                        num=_.get('num'),
                        lengh=_.get('length'),
                        status=1
                    )
                    objs.append(o)
                db.session.add_all(objs)
                db.session.commit()

            elif origin_details and not new_details:
                # 删除
                for _ in origin_details:
                    db.session.query(OrderDetail).filter(OrderDetail.id == _[0]).update({OrderDetail.status: 2})
                db.session.commit()
            else:
                # 更新
                origin_detail_ids = [_[0] for _ in origin_details]
                objs = list()
                for _ in new_details:
                    if not _.get('id') or _.get('id') not in origin_detail_ids:
                        o = OrderDetail(
                            order_id=order_id,
                            type_id=_.get('type_id'),
                            item_id=_.get('item_id'),
                            price=_.get('price'),
                            num=_.get('num'),
                            lengh=_.get('length'),
                            status=1
                        )
                        objs.append(o)
                    else:
                        if _.get('status', 1) != 2:
                            db.session.query(OrderDetail) \
                                .filter(OrderDetail.id == _.get('id')) \
                                .update({OrderDetail.type_id: _.get("type_id"),
                                         OrderDetail.item_id: _.get("item_id"),
                                         OrderDetail.price: _.get("price"),
                                         OrderDetail.num: _.get("num"),
                                         OrderDetail.lengh: _.get("length")
                                         })
                        else:
                            db.session.query(OrderDetail).filter(OrderDetail.id == _.get('id')).update(
                                {OrderDetail.status: 2})
                if objs:
                    db.session.add_all(objs)
                db.session.commit()
        return jsonify(base_success_res({}))
    except Exception as e:
        print(e)
        return jsonify(base_fail_res(e.args, {}))


@inter.route("/orders", methods=['GET'])
# @admin_login_req
def orders():
    order_id = request.args.get('order_id')
    order_no = request.args.get('order_no')
    if not order_id and not order_no:
        return jsonify(base_fail_res("miss params", None))
    base_query = db.session.query(Order, Guest).join(Guest, Order.guest_id == Guest.user_id)
    if order_id:
        base_query = base_query.filter(Order.id == order_id)
    if order_no:
        base_query = base_query.filter(Order.order_no == order_no)
    order_base = base_query.first()
    if not order_base:
        return jsonify(base_fail_res("订单号", {"items": []}))
    details = db.session.query(GoodsType.id, TypeItem.id, OrderDetail.price, OrderDetail.num,
                               TypeItem.unit, GoodsType.name, TypeItem.item_name,
                               OrderDetail.lengh, OrderDetail.id) \
        .join(GoodsType, GoodsType.id == OrderDetail.type_id) \
        .join(TypeItem, TypeItem.id == OrderDetail.item_id) \
        .filter(order_base[0].id == OrderDetail.order_id, OrderDetail.status == 1).all()
    order_base = {
        "id": order_base[0].id,
        "order_no": order_base[0].order_no,
        "guest_id": order_base[1].user_id,
        "guest_name": order_base[1].user_name,
        "description": order_base[0].description,
        "total": order_base[0].total,
        "pay": order_base[0].pay,
        "unpay": order_base[0].unpay,
        "details": []
    }
    if details:
        items = list()
        item = {}
        for i in details:
            item['type_id'] = i[0]
            item['item_id'] = i[1]
            item['price'] = i[2]
            item['num'] = i[3]
            item['unit'] = i[4]
            item['type_name'] = i[5]
            item['item_name'] = i[6]
            item['length'] = i[7]
            item['id'] = i[8]
            items.append(item)
        order_base['details'] = items
    return jsonify(base_success_res({"order": order_base}))


@inter.route("/types", methods=['GET'])
# @admin_login_req
def types():
    type_id = str(request.args.get('id', ''))
    if not type_id:
        page_data = GoodsType.query.filter(GoodsType.status == 1) \
            .order_by(GoodsType.id.desc()).all()
    else:
        page_data = GoodsType.query.filter(GoodsType.status == 1, GoodsType.id == type_id) \
            .order_by(GoodsType.id.desc()).all()
    if not page_data:
        return base_success_res({"items": []})
    return jsonify(base_success_res({"items": [{"id": _.id, "type_name": _.name} for _ in page_data]}))


@inter.route("/type_items", methods=['GET'])
@admin_login_req
def type_items():
    type_id = str(request.args.get('type_id', ''))
    item_id = str(request.args.get('item_id', ''))
    base_query = TypeItem.query.filter(GoodsType.status == 1, TypeItem.status == 1)
    if type_id:
        base_query = base_query.filter(TypeItem.goods_type_id == type_id)
    if item_id:
        base_query = base_query.filter(TypeItem.item_id == item_id)
    page_data = base_query.order_by(GoodsType.id.desc()).all()
    if not page_data:
        return base_success_res({"items": []})
    #  返回的unit为商品规格单位，可以根据单位是不是米来确认是否显示长度的输入框
    return jsonify(base_success_res(
        {"items": [{"id": _.id, "item_name": _.item_name, "type_id": _.goods_type_id, "unit": _.unit} for _ in
                   page_data]}))


@inter.route("/guests", methods=['GET'])
# @admin_login_req
def guests():
    guest_id = str(request.args.get('guest_id', ''))
    guest_name = str(request.args.get('guest_name', ''))
    base_query = Guest.query.filter(Guest.status == 1)
    if guest_id:
        base_query = base_query.filter(Guest.user_id == guest_id)
    if guest_name:
        base_query = base_query.filter(Guest.user_name == guest_name)
    page_data = base_query.order_by(Guest.user_id.desc()).all()
    if not page_data:
        return base_success_res({"items": []})
    #  返回的unit为商品规格单位，可以根据单位是不是米来确认是否显示长度的输入框
    return jsonify(base_success_res(
        {"items": [{"guest_id": _.user_id, "guest_name": _.user_name} for _ in
                   page_data]}))


@inter.route("/user_pay_statistics", methods=['GET'])
# @admin_login_req
def user_pay_statistics():
    guest_name = str(request.args.get('name', ''))
    order_no = str(request.args.get('order_no', ''))
    if not guest_name and not order_no:
        return jsonify(base_fail_res("miss params", None))
    start_time = request.args.get('start_time', '')
    end_time = request.args.get('end_time', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    result = user_statistics(guest_name, order_no, start_time, end_time)
    #  返回的unit为商品规格单位，可以根据单位是不是米来确认是否显示长度的输入框
    return jsonify(base_success_res(result)) if result.get('result_code') != 'error' else jsonify(result)


@inter.route("/order_statistics", methods=['GET'])
# @admin_login_req
def order_statistics():
    start_time = request.args.get('start_time', '')
    end_time = request.args.get('end_time', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    result = compute_order_statistics(start_time, end_time)
    #  返回的unit为商品规格单位，可以根据单位是不是米来确认是否显示长度的输入框
    return jsonify(base_success_res(result)) if result.get('result_code') != 'error' else jsonify(result)


@inter.route("/order_print", methods=['GET'])
# @admin_login_req
def order_print():
    order_id = str(request.args.get('order_id', ''))
    if not order_id:
        return jsonify(base_fail_res("miss params order_id", None))
    base_info = db.session.query(Order, Guest) \
        .join(Guest, Order.guest_id == Guest.user_id) \
        .filter(Order.id == order_id).all()
    if not base_info or not base_info[0]:
        return jsonify(base_fail_res("order_id invalid", None))
    print_info = print_template()
    print_info['guest_name'] = base_info[0][1].user_name
    print_info['guest_phone'] = base_info[0][1].user_phone
    print_info['order_no'] = base_info[0][0].order_no
    print_info['amount_receivable'] = base_info[0][0].total
    print_info['out_date'] = datetime.datetime.strftime(base_info[0][0].add_time, "%Y/%m/%d")

    detail_data = db.session.query(OrderDetail, TypeItem, GoodsType) \
        .join(TypeItem, TypeItem.id == OrderDetail.item_id) \
        .join(GoodsType, GoodsType.id == OrderDetail.type_id) \
        .filter(OrderDetail.status == 1, OrderDetail.order_id == order_id).all()
    details = []
    for i in detail_data:
        detail = {}
        order_detail = i[0]
        type_item = i[1]
        goods_type = i[2]
        detail['goods_type'] = goods_type.name
        detail['type_item'] = type_item.item_name
        num = float(order_detail.num if order_detail.num else 0)
        detail['num'] = num
        price = float(order_detail.price if order_detail.price else 0)
        detail['price'] = "￥{}".format(price)
        if type_item.unit == '1':
            detail['length'] = order_detail.lengh if order_detail.lengh else 0
            detail['total_length'] = detail.get('length') * detail.get('num')
            detail['item_total'] = "￥{}".format(detail.get('length') * num * price)
        else:
            detail['item_total'] = "￥{}".format(num * price)
        details.append(detail)
    print_info['details'] = details
    return jsonify(base_success_res(print_info))


def print_template():
    return {
        'title': '南阳恒宇彩板 岩棉复合板 单瓦 楼承板 C Z 型钢',
        'sub_title': '黄石山力 天津新宇彩卷南阳总代理 销售出货单',
        'connect': '南阳兴达钢材市场 电话：0377-63150159 68060601',
        'out_date': '',
        'out_status': '已出货',
        'order_no': '',
        'guest_name': '',
        'check': '',
        'guest_phone': '',
        'pay': '',
        'amount_receivable': '',
        'discount_amount': '',
        'details': {

        }
    }
