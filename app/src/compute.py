import datetime
import time

import sqlalchemy
from sqlalchemy import func
from app.apps import db
from app.models import Order, Guest


def user_statistics(guest_name=None, order_no=None, start_time=None, end_time=None):
    if not guest_name and not order_no:
        return {
            "msg": "miss params",
            "data": None,
            "result_code": 'error',
            "server_time": int(time.time())
        }
    end_time = end_time if end_time else time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    base_query = db.session.query(func.sum(Order.total), func.sum(Order.pay),
                                  func.sum(Order.unpay), func.count(Order.id)) \
        .join(Guest, Order.guest_id == Guest.user_id)
    if guest_name:
        base_query = base_query.filter(Guest.user_name == guest_name)
    if order_no:
        base_query = base_query.filter(Order.order_no == order_no)
    if end_time and start_time:
        base_query = base_query.filter(Order.add_time < end_time, Order.add_time > start_time)
    elif end_time:
        base_query = base_query.filter(Order.add_time < end_time)
    page_data = base_query.order_by(Guest.user_id.desc()).all()
    return {
        "total": page_data[0][0],
        "pay": page_data[0][1],
        "unpay": page_data[0][2],
        "total_order": page_data[0][3],
    }


def compute_order_statistics(start_time=None, end_time=None):
    end_time = end_time if end_time else time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    order_query = db.session.query(func.sum(Order.total), func.sum(Order.pay),
                                   func.sum(Order.unpay), func.count(Order.id)) \
        .join(Guest, Order.guest_id == Guest.user_id)
    if end_time and start_time:
        order_query = order_query.filter(Order.add_time < end_time, Order.add_time > start_time)
    elif end_time:
        order_query = order_query.filter(Order.add_time < end_time)
    order_data = order_query.order_by(Guest.user_id.desc()).all()
    return {
        "total": order_data[0][0],
        "pay": order_data[0][1],
        "unpay": order_data[0][2],
        "total_order": order_data[0][3],
    }


def compute_order_num_statistics(start_time=None, end_time=None, days=30):
    end_time = end_time if end_time else time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    order_query = db.session.query(func.date_format(Order.add_time, '%Y-%m-%d').label('order_date'),
                                   func.count(Order.id))
    if not start_time:
        base_timestamp = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(base_timestamp - days * 24 * 60 * 60))
    order_query = order_query.filter(Order.add_time < end_time, Order.add_time > start_time).group_by(
        func.date_format(Order.add_time, '%Y-%m-%d')) \
        .order_by(sqlalchemy.asc('order_date'))
    order_data = order_query.all()
    return order_data


def home_order_statistics():
    today = datetime.date.today()
    this_week_first = today - datetime.timedelta(days=today.weekday() + 7)
    this_month_first = datetime.date(today.year, today.month, 1)
    today_order_data = db.session.query(func.count(Order.id)).filter(
        Order.add_time >= '{} 00:00:00'.format(today)).all()
    week_order_data = db.session.query(func.count(Order.id)).filter(
        Order.add_time >= '{} 00:00:00'.format(this_week_first)).all()
    month_order_data = db.session.query(func.count(Order.id)).filter(
        Order.add_time >= '{} 00:00:00'.format(this_month_first)).all()
    return {"current": today_order_data[0][0], "this_week": week_order_data[0][0], "this_month": month_order_data[0][0]}


def money_statistics():
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    base_query = db.session.query(func.sum(Order.total), func.sum(Order.pay), func.sum(Order.unpay)) \
        .join(Guest, Order.guest_id == Guest.user_id).filter(Order.add_time < end_time)
    page_data = base_query.order_by(Guest.user_id.desc()).all()
    return page_data


def string_money_statistics(page_data):
    return {
        "total": '￥{:0,.2f}'.format(page_data[0][0]),
        "pay": '￥{:0,.2f}'.format(page_data[0][1]),
        "un_pay": '￥{:0,.2f}'.format(page_data[0][2])
    }


def num_money_statistics(page_data):
    return {
        "total": round(page_data[0][0], 2),
        "pay": round(page_data[0][1], 2),
        "un_pay": round(page_data[0][2], 2)
    }
