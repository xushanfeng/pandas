from functools import wraps
from io import BytesIO
from werkzeug.security import generate_password_hash

from app.admin.forms import Login, ResetPassword, GuestForm, GuestSearch, GoodsTypeSearch, GoodsTypeForm, \
    TypeItemSearch, TypeItemForm, OrderSearch
from app.apps import db
from app.admin import admin
from flask import render_template, make_response, session, redirect, url_for, request, flash
from app.admin.uilt import get_verify_code
from app.constant.const import PAGE_LIMIT, SEX
from app.models import User, Guest, GoodsType, TypeItem, Order
from app.utils.doc import admin_login_req


def admin_power(f):
    @wraps(f)
    def admin_function(*args, **kwargs):
        if session['power'] != 'root':
            return render_template("admin/errorroot.html")
        return f(*args, **kwargs)

    return admin_function


# 登陆模块
@admin.route("/login/", methods=["GET", "POST"])
def login():
    """登陆路由"""

    form = Login()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(user_count=data['account']).first()
        if user is None:
            flash("账号错误")
            return redirect(url_for("admin.login"))
        if not user.check_pwd(data['pwd']):
            flash("密码错误")
            return redirect(url_for("admin.login"))
        if session.get('image').lower() != form.verify_code.data.lower():
            flash('Wrong verify code.')
            return redirect(url_for("admin.login"))
        session["admin"] = data['account']
        session["admin_id"] = user.user_id
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)


# 验证码路由
@admin.route('/code/')
def code():
    """生成验证码图片流"""
    image, img_code = get_verify_code()
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    session['image'] = img_code
    return response


# 客户管理
@admin.route("/guests/<int:page>", methods=["GET", "POST"])
@admin_login_req
def guests(page=None):
    form = GuestSearch()
    page = page if page is not None else 1
    guest_query = Guest.query.order_by(Guest.user_id.desc()).filter(Guest.status == 1)
    name = str(form.data.get('name')).strip() if form.data.get('name') else None
    phone = str(form.data.get('phone')).strip() if form.data.get('phone') else None
    if name:
        guest_query = guest_query.filter(Guest.user_name.like('%{}%'.format(name)))
    if form.data.get('phone'):
        guest_query = guest_query.filter(Guest.user_phone.like('%{}%'.format(phone)))
    page_data = guest_query.filter().paginate(page=page, per_page=PAGE_LIMIT)
    return render_template("admin/guests.html", form=form, page_data=page_data)


# 添加客户
@admin.route("/add_guest", methods=["GET", "POST"])
def add_guest():
    """添加客户"""
    edit = request.args.get('edit')
    user_id = request.args.get('user_id')
    form = GuestForm()
    if not edit:
        if form.validate_on_submit():
            data = form.data
            names = Guest.query.filter_by(user_name=data['name']).count()
            if names == 1:
                flash('添加失败')
                return redirect(url_for("admin.guests"))
            ses = ['', '男', '女']
            guest = Guest(
                user_name=data['name'],
                user_sex=ses[data['sex']],
                user_phone=data['phone'],
                user_mail=data['email'],
                addr=data['addr']
            )
            db.session.add(guest)
            db.session.commit()
            flash("添加客户")
    elif request.method.lower() == "get" and edit:
        user = Guest.query.filter_by(user_id=user_id).first()
        form = GuestForm(name=user.user_name,
                         phone=user.user_phone,
                         email=user.user_mail,
                         sex=SEX.get(user.user_sex),
                         id=user.user_id,
                         addr=user.addr,
                         edit=True)
    elif request.method.lower() == "post" and edit:
        if form.validate_on_submit():
            data = form.data
            check_guest = Guest.query.filter_by(user_name=data['name']).first()
            if check_guest and str(check_guest.user_id) != str(user_id):
                flash('编辑失败')
                return redirect(url_for("admin.add_guest"))
            ses = ['', '男', '女']
            db.session.query(Guest).filter(Guest.user_id == user_id) \
                .update({Guest.user_name: data['name'],
                         Guest.user_sex: ses[data['sex']],
                         Guest.user_phone: data['phone'],
                         Guest.addr: data['addr'],
                         Guest.user_mail: data['email']})
            db.session.commit()
            flash("编辑客户")
    return render_template("admin/add_guest.html", form=form)


# 材质管理
@admin.route("/category/<int:page>", methods=["GET", "POST"])
@admin_login_req
def category(page=None):
    form = GoodsTypeSearch()
    page = page if page is not None else 1
    name = str(form.data.get('name')).strip() if form.data.get('name') else None
    goods_type_query = GoodsType.query.order_by(GoodsType.id.desc()).filter(GoodsType.status == 1)
    if name:
        goods_type_query = goods_type_query.filter(GoodsType.name.like('%{}%'.format(name)))
    page_data = goods_type_query.paginate(page=page, per_page=PAGE_LIMIT)
    return render_template("admin/categories.html", form=form, page_data=page_data)


# 添加大类
@admin.route("/add_goods_type/", methods=["GET", "POST"])
def add_goods_type():
    """添加大类"""
    type_id = request.args.get('type_id')
    edit = request.args.get('edit')
    form = GoodsTypeForm()
    if not edit:
        if form.validate_on_submit():
            data = form.data
            names = GoodsType.query.filter_by(name=data['name'], status=1).count()
            if names == 1:
                flash('添加失败')
                return redirect(url_for("admin.add_goods_type"))
            goods_type = GoodsType(
                name=data['name'],
                description=data['description']
            )
            db.session.add(goods_type)
            db.session.commit()
            flash("添加大类")
            return redirect(url_for("admin.category", page=1))
    elif request.method.lower() == 'get' and edit:
        types = GoodsType.query.filter(GoodsType.id == type_id).first()
        if not types:
            return render_template("admin/404.html")
        form = GoodsTypeForm(id=types.id,
                             name=types.name,
                             description=types.description)
        return render_template("admin/add_goods_type.html", form=form)
    elif request.method.lower() == 'post' and edit:
        if form.validate_on_submit():
            data = form.data
            goods_type = GoodsType.query.filter_by(name=data['name']).first()
            if goods_type and str(goods_type.id) != str(type_id):
                flash('编辑失败')
                return redirect(url_for("admin.add_goods_type"))
            db.session.query(GoodsType).filter(GoodsType.id == type_id) \
                .update({GoodsType.name: data['name'],
                         GoodsType.description: data['description']})
            db.session.commit()
            flash("编辑类型")
            form = GoodsTypeSearch()
            page_data = GoodsType.query.filter(GoodsType.status == 1).order_by(GoodsType.id.desc()).paginate(page=1,
                                                                                                             per_page=PAGE_LIMIT)
            return render_template("admin/categories.html", form=form, page_data=page_data)
    return render_template("admin/add_goods_type.html", form=form)


# 材质小类
@admin.route("/type_item/<int:page>", methods=["GET", "POST"])
@admin_login_req
def type_item(page=None):
    form = TypeItemSearch()
    page = page if page is not None else 1
    name = str(form.data.get('name')) if form.data.get('name') else None
    item_query = db.session.query(TypeItem.id, TypeItem.item_name, TypeItem.description, TypeItem.goods_type_id,
                                  GoodsType.name).join(GoodsType, GoodsType.id == TypeItem.goods_type_id)
    if name:
        item_query = item_query.filter(TypeItem.item_name.like('%{}%'.format(name)))
    page_data = item_query.filter(TypeItem.status == 1).order_by(TypeItem.id.desc()).paginate(page=page,
                                                                                              per_page=PAGE_LIMIT)
    return render_template("admin/type_items.html", form=form, page_data=page_data)


# 添加小类
@admin.route("/add_type_item/", methods=["GET", "POST"])
def add_type_item():
    """添加小类"""
    edit = request.args.get('edit')
    item_id = request.args.get('id')
    form = TypeItemForm()
    if not edit and not item_id:
        if form.validate_on_submit():
            data = form.data
            names = TypeItem.query.filter_by(item_name=data['name'], status=1).count()
            if names == 1:
                flash('添加失败')
                return redirect(url_for("admin.add_type_item"))
            item = TypeItem(
                item_name=data['name'],
                goods_type_id=data['type_name'],
                unit=data['unit'],
                description=data['description'],
                status=1
            )
            db.session.add(item)
            db.session.commit()
            flash("添加小类")
    elif request.method.lower() == 'get' and edit:
        items = TypeItem.query.filter(TypeItem.id == item_id).first()
        if not items:
            return render_template("admin/404.html")
        form = TypeItemForm(id=items.id,
                            type_name=items.goods_type_id,
                            name=items.item_name,
                            unit=items.unit,
                            description=items.description)
        return render_template("admin/add_type_item.html", form=form)
    elif request.method.lower() == 'post' and edit:
        if form.validate_on_submit():
            data = form.data
            item = TypeItem.query.filter_by(item_name=data['name'], status=1).first()
            if item and str(item.id) != str(item_id):
                flash('编辑失败')
                return redirect(url_for("admin.add_goods_type"))
            db.session.query(TypeItem).filter(TypeItem.id == item_id) \
                .update({TypeItem.item_name: data['name'],
                         TypeItem.goods_type_id: data['type_name'],
                         TypeItem.unit: data['unit'],
                         TypeItem.description: data['description']})
            db.session.commit()
            flash("编辑类型")
            form = TypeItemSearch()
            page_data = db.session.query(TypeItem.id, TypeItem.item_name, TypeItem.description, TypeItem.goods_type_id,
                                         GoodsType.name) \
                .join(GoodsType, GoodsType.id == TypeItem.goods_type_id) \
                .filter(TypeItem.status == 1) \
                .order_by(TypeItem.id.desc()) \
                .paginate(page=1, per_page=PAGE_LIMIT)
            return render_template("admin/type_items.html", form=form, page_data=page_data)
    return render_template("admin/add_type_item.html", form=form)


# 出库单
@admin.route("/order/<int:page>", methods=["GET", "POST"])
@admin_login_req
def order(page=None):
    form = OrderSearch()
    page = page if page is not None else 1
    name = str(form.data.get('name')).strip() if form.data.get('name') else None
    order_query = db.session.query(Order.id, Order.order_no, Order.total, Order.pay, Order.unpay, Guest.user_name)\
        .join(Guest, Guest.user_id == Order.guest_id)
    if name:
        order_query = order_query.filter(Guest.user_name.like('%{}%'.format(name)))
    page_data = order_query.order_by(Order.id.desc()).paginate(page=page, per_page=PAGE_LIMIT)
    return render_template("admin/order.html", form=form, page_data=page_data)


# 添加出库单
@admin.route("/add_order/", methods=["GET"])
def add_order():
    """添加出库单"""
    guests = Guest.query.filter(Guest.status == 1).all()
    typeItems = TypeItem.query.filter(GoodsType.status == 1, TypeItem.status == 1).all()
    types = GoodsType.query.filter(GoodsType.status == 1).order_by(GoodsType.id.desc()).all()
    return render_template("admin/add_order.html", guests=guests, types=types, type_items=typeItems)


# 首页
@admin.route("/")
@admin_login_req
def index():
    return render_template("admin/index.html", name=session["admin"])


@admin.route("/workPlatform/")
@admin_login_req
def workPlatform():
    # purchases = len(Purchase.query.all())
    # saless = len(sales.query.all())
    # warehouses = len(warehouse.query.all())
    names = {"purchases": 2, "saless": 2, "warehouses": 1}
    return render_template("admin/workPlatform.html", name=session["admin"], names=names)


# 退出
@admin.route('/logout')
@admin_login_req
def logout():
    session.pop('admin', None)
    return redirect(url_for("admin.login"))


# 基本模块
@admin.route("/person_detail/", methods=['GET', 'POST'])
@admin_login_req
def person_detail():
    form = ResetPassword()
    usermessage = User.query.filter(User.user_count == session["admin"]).first()
    admin = User.query.filter_by(user_count=usermessage.user_count).first()
    if form.validate_on_submit():
        if not admin.check_pwd(form.data['account']):
            flash('旧密码错误，请联系管理员修改')
            return render_template("admin/person_detail.html", form=form, usermessage=usermessage)
        admin.user_pwd = generate_password_hash((form.data['pwd']))
        try:
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        session.pop('admin', None)
        return 'Success'

    return render_template("admin/person_detail.html", form=form, usermessage=usermessage)


# 删除客户
@admin.route("/del_guest/", methods=["GET"])
@admin_login_req
def del_guest():
    guest_user_id = request.args.get('id')
    try:
        db.session.query(Guest).filter(Guest.user_id == guest_user_id).update({Guest.status: 2})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print("del error, error info:", e)
    return "success"


# 删除类型
@admin.route("/del_type/", methods=["GET"])
@admin_login_req
def del_type():
    type_id = request.args.get('id')
    try:
        db.session.query(GoodsType).filter(GoodsType.id == type_id).update({GoodsType.status: 2})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        db.session.close()
        print("del error, error info:", e)
    return "success"


# 删除小类
@admin.route("/del_type_item/", methods=["GET"])
@admin_login_req
def del_type_item():
    item_id = request.args.get('id')
    try:
        db.session.query(TypeItem).filter(TypeItem.id == item_id).update({TypeItem.status: 2})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        db.session.close()
        print("del error, error info:", e)
    return "success"
