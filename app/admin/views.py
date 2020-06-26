import time
from functools import wraps
from io import BytesIO
from flask_mail import Message
from werkzeug.security import generate_password_hash

from app.admin.forms import Login, ResetPassword, GuestForm, GuestSearch, GoodsTypeSearch, GoodsTypeForm, \
    TypeItemSearch, TypeItemForm, OrderSearch, OrderForm
from app.apps import db, mail
from app.admin import admin
from flask import render_template, make_response, session, redirect, url_for, request, flash
from app.admin.uilt import get_verify_code
from app.constant.const import PAGE_LIMIT, SEX
from app.models import User, Guest, GoodsType, TypeItem, Order, OrderDetail


def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


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


# 注册路由
@admin.route("/register/", methods=["GET", "POST"])
def register():
    """注册路由"""
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        names = User.query.filter_by(user_count=data['account']).count()
        if names == 1:
            flash('注册失败')
            return redirect(url_for("admin.register"))
        ses = ['', '男', '女']
        names = User(
            user_count=data['account'],
            user_pwd=generate_password_hash((data['pwd'])),
            user_name=data['name'],
            user_sex=ses[data['sex']],
            user_phone=data['phone'],
            user_mail=data['mail']
        )

        db.session.add(names)
        db.session.commit()
        flash("注册成功")

        return redirect(url_for("admin.login"))
    return render_template("admin/register.html", form=form)


# 客户管理
@admin.route("/guests/<int:page>", methods=["GET", "POST"])
@admin_login_req
def guests(page=None):
    form = GuestSearch()
    page = page if page is not None else 1
    if (form.data['name'] is None or form.data['name'] == '') and (
            form.data['phone'] is None or form.data['phone'] == ''):
        page_data = Guest.query.order_by(
            Guest.user_id.desc()
        ).filter(Guest.status == 1).paginate(page=page, per_page=PAGE_LIMIT)

    elif (form.data['name'].strip()) and (form.data['phone'] is None or form.data['phone'] == ''):
        page_data = Guest.query.order_by(
            Guest.user_id.desc()
        ).filter(form.data['name'] == Guest.user_name, Guest.status == 1).paginate(page=page, per_page=PAGE_LIMIT)
    elif (form.data['name'] is None or form.data['name'] == '') and (
            form.data['phone'].strip()):
        page_data = Guest.query.order_by(
            Guest.user_id.desc()
        ).filter(form.data['phone'] == Guest.user_phone).paginate(page=page, per_page=PAGE_LIMIT)
    elif form.data.get('name') and form.data.get('phone'):
        page_data = Guest.query.order_by(
            Guest.user_id.desc()
        ).filter(form.data['phone'] == Guest.user_phone, form.data['name'] == Guest.user_name,
                 Guest.status == 1).paginate(page=page,
                                             per_page=PAGE_LIMIT)
    else:
        return render_template("admin/404.html")
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
                user_mail=data['email']
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
                         Guest.user_mail: data['email']})
            db.session.commit()
            flash("编辑客户")
    return render_template("admin/add_guest.html", form=form)


# 添加客户
@admin.route("/edit_guest/", methods=["GET", "POST"])
def edit_guest():
    """添加客户"""
    form = GuestForm()
    if form.validate_on_submit():
        data = form.data
        names = Guest.query.filter_by(user_name=data['name']).count()
        if names == 1:
            flash('添加失败')
            return redirect(url_for("admin.add_guest"))
        ses = ['', '男', '女']
        guest = Guest(
            user_name=data['name'],
            user_sex=ses[data['sex']],
            user_phone=data['phone'],
            user_mail=data['email']
        )
        db.session.add(guest)
        db.session.commit()
        flash("添加客户")
    return render_template("admin/add_guest.html", form=form)


# 材质管理
@admin.route("/category/<int:page>", methods=["GET", "POST"])
@admin_login_req
def category(page=None):
    form = GoodsTypeSearch()
    page = page if page is not None else 1
    if form.data.get('name') is None or not str(form.data.get('name')).strip():
        page_data = GoodsType.query.order_by(GoodsType.id.desc()).paginate(page=page, per_page=PAGE_LIMIT)
    else:
        page_data = GoodsType.query.order_by(GoodsType.id.desc()).filter(form.data['name'] == GoodsType.name).paginate(
            page=page, per_page=PAGE_LIMIT)
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
            names = GoodsType.query.filter_by(name=data['name']).count()
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
    elif request.method.lower() == 'get' and edit:
        types = GoodsType.query.filter(GoodsType.id == type_id).first()
        if not types:
            return render_template("admin/404.html")
        form = GoodsTypeForm(id=types.id,
                             name=types.name,
                             description=types.description)
    elif request.method.lower() == 'post' and edit:
        if form.validate_on_submit():
            data = form.data
            goods_type = GoodsType.query.filter_by(name=data['name']).first()
            if goods_type and str(goods_type.user_id) != str(type_id):
                flash('编辑失败')
                return redirect(url_for("admin.add_goods_type"))
            db.session.query(GoodsType).filter(GoodsType.id == type_id) \
                .update({GoodsType.name: data['name'],
                         GoodsType.description: data['description']})
            db.session.commit()
            flash("编辑类型")
    return render_template("admin/add_goods_type.html", form=form)


# 材质小类
@admin.route("/type_item/<int:page>", methods=["GET", "POST"])
@admin_login_req
def type_item(page=None):
    form = TypeItemSearch()
    page = page if page is not None else 1
    if form.data.get('name') is None or not str(form.data.get('name')).strip():
        page_data = db.session.query(TypeItem.id, TypeItem.item_name, TypeItem.description, GoodsType.id,
                                     GoodsType.name) \
            .join(GoodsType, GoodsType.id == TypeItem.goods_type_id).order_by(TypeItem.id.desc()) \
            .paginate(page=page, per_page=PAGE_LIMIT)

    else:
        page_data = db.session.query(TypeItem.id, TypeItem.item_name, TypeItem.description, GoodsType.name,
                                     GoodsType.id) \
            .join(GoodsType, GoodsType.id == TypeItem.goods_type_id) \
            .order_by(TypeItem.id.desc()) \
            .filter(form.data['name'] == TypeItem.item_name, ) \
            .paginate(page=page, per_page=PAGE_LIMIT)
    return render_template("admin/type_items.html", form=form, page_data=page_data)


# 添加小类
@admin.route("/add_type_item/", methods=["GET", "POST"])
def add_type_item():
    """添加小类"""
    form = TypeItemForm()
    if form.validate_on_submit():
        data = form.data
        names = TypeItem.query.filter_by(item_name=data['name']).count()
        if names == 1:
            flash('添加失败')
            return redirect(url_for("admin.add_type_item"))
        item = TypeItem(
            item_name=data['name'],
            goods_type_id=data['type_name'],
            description=data['description']
        )
        db.session.add(item)
        db.session.commit()
        flash("添加小类")
    return render_template("admin/add_type_item.html", form=form)


# 出库单
@admin.route("/order/<int:page>", methods=["GET", "POST"])
@admin_login_req
def order(page=None):
    form = OrderSearch()
    page = page if page is not None else 1
    if form.data.get('name') is None or not str(form.data.get('name')).strip():
        page_data = Order.query \
            .paginate(page=page, per_page=PAGE_LIMIT)

    else:
        page_data = Order.query \
            .order_by(Order.id.desc()) \
            .filter(form.data['order_no'] == Order.order_no, ) \
            .paginate(page=page, per_page=PAGE_LIMIT)
    return render_template("admin/order.html", form=form, page_data=page_data)


# 添加出库单
@admin.route("/add_order/", methods=["GET", "POST"])
def add_order():
    """添加出库单"""
    form = OrderForm()
    print(form.data)
    if form.validate_on_submit():
        data = form.data
        order_no = Order.query.filter_by(item_name=data['order_no']).count()
        if order_no == 1:
            flash('添加失败')
            return redirect(url_for("admin.add_order"))
        order = Order(
            order_no=time.strftime("%y%m%d%H%M%s", time.localtime()),
            guest_id=data['description'],
            description=data['description'],
            operator_id=session.get('admin'),
        )
        db.session.add(order)
        for item in form.details.data:
            new_item = OrderDetail(**item)
            order.order_detail.append(new_item)
        db.session.commit()
        flash("添加小类")
    return render_template("admin/add_order.html", form=form)


# 忘记密码路由
@admin.route("/forgetpws/")
def forgetpws():
    pass


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


#
# 忘记密码
@admin.route("/wjmm/", methods=['GET', 'POST'])
def wjmm():
    form = wjpasswd()
    if form.validate_on_submit():
        usermessage = User.query.filter(User.user_count == form.data["countname"]).first()
        if usermessage is None:
            flash("账号错误！")
            return render_template("admin/wjmm.html", form=form)
        admin = User.query.filter_by(user_count=usermessage.user_count).first()

        if admin.user_mail != form.data['account']:
            flash('请输入正确的邮箱地址，或联系管理员修改')
            return render_template("admin/wjmm.html", form=form)

        admin.user_pwd = generate_password_hash((form.data['pwd']))
        mails = []
        mails.append(form.data['account'])
        try:
            msg = Message('修改密码通知', sender='gchase@163.com', recipients=mails)
            msg.html = '<span>尊敬的</span>' + usermessage.user_name + '，您好：<br>您在we商贸中申请找回密码<br><b style="background-color: #FF0000">重设密码已完成,若非本人操作</b><br>请及时联系管理员修改<b>ganiner@163.com</b>'
            mail.send(msg)
            flash("修改成功")
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        return redirect(url_for('admin.login'))
    return render_template("admin/wjmm.html", form=form)


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
