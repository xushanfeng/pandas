import time

import sqlalchemy
from pyecharts import Line
from pyecharts_javascripthon.api import TRANSLATOR
from sqlalchemy import func

from app.apps import db
from app.models import Order


def lines():
    line = line_chart()
    javascript_snippet = TRANSLATOR.translate(line.options)
    return line, javascript_snippet


def line_chart(end_time=None, start_time=None):
    end_time = end_time if end_time else time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    order_query = db.session.query(func.date_format(Order.add_time, '%Y-%m-%d').label('order_date'),
                                   func.count(Order.id))
    if not start_time:
        base_timestamp = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(base_timestamp - 30 * 24 * 60 * 60))
    order_query = order_query.filter(Order.add_time < end_time, Order.add_time > start_time).group_by(
        func.date_format(Order.add_time, '%Y-%m-%d')) \
        .order_by(sqlalchemy.asc('order_date'))
    order_data = order_query.all()
    attr = [i for _, i in order_data]
    v1 = [j for j, _ in order_data]
    line = Line("近30天订单统计")
    line.add("", v1, attr, is_stack=True, is_smooth=True, is_fill=True)
    return line