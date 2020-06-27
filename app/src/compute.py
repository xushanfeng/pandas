import time

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
