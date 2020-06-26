import datetime
from .apps import db


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    user_count = db.Column(db.String(100), unique=True)
    user_name = db.Column(db.String(100), unique=True)
    user_sex = db.Column(db.String(100))
    user_pwd = db.Column(db.String(100))
    user_mail = db.Column(db.String(100))
    user_phone = db.Column(db.String(100))
    user_addtime = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    user_photo = db.Column(db.String(100))
    user_ispass = db.Column(db.Integer)

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.user_pwd, pwd)


class Guest(db.Model):
    __tablename__ = 'guest'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), unique=True)
    user_sex = db.Column(db.String(100))
    user_mail = db.Column(db.String(100))
    addr = db.Column(db.String(100))
    user_phone = db.Column(db.String(100))
    status = db.Column(db.Integer)
    user_addtime = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    operator_id = db.Column(db.Integer)
    pay = db.Column(db.Integer)
    unpay = db.Column(db.Integer)


class GoodsType(db.Model):
    __tablename__ = 'goods_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(300), unique=True)
    add_time = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    status = db.Column(db.Integer)
    operator_id = db.Column(db.Integer)


class TypeItem(db.Model):
    __tablename__ = 'type_item'
    id = db.Column(db.Integer, primary_key=True)
    goods_type_id = db.Column(db.Integer, unique=True)
    status = db.Column(db.Integer, unique=True)
    item_name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(300), unique=True)
    add_time = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    operator_id = db.Column(db.Integer)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(100), unique=True)
    guest_id = db.Column(db.Integer, unique=True)
    pay = db.Column(db.Integer, unique=True)
    unpay = db.Column(db.Integer, unique=True)
    total = db.Column(db.Integer, unique=True)
    description = db.Column(db.String(300), unique=True)
    add_time = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    operator_id = db.Column(db.Integer)


class OrderDetail(db.Model):
    __tablename__ = 'order_detail'
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, unique=True)
    item_id = db.Column(db.Integer, unique=True)
    price = db.Column(db.Integer, unique=True)
    num = db.Column(db.Integer, unique=True)
    unit = db.Column(db.String(10), unique=True)
    add_time = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    operator_id = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship('Order', backref=db.backref('order_detail', lazy='dynamic', collection_class=list))
