# 登陆表单
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FieldList, FormField, \
    IntegerField, RadioField
from wtforms.validators import DataRequired, ValidationError

from app.constant.const import UNIT
from app.models import GoodsType, Guest, TypeItem


class Login(FlaskForm):
    account = StringField(
        label="用户名",
        validators=[
            DataRequired()
        ],
        description="账号",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入账号！",
        }

    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired()
        ],
        description="密码",
        render_kw={
            "type": "password",
            "class": "layui-input",
            "placeholder": "请输入密码！",
            "lay-verify": "required",
        }
    )
    verify_code = StringField(
        label='验证码',
        validators=[
            DataRequired()
        ],
        description="验证码",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input-inline",
            "placeholder": "请输入验证码！",
        }
    )

    submit = SubmitField(
        "登录",
        render_kw={
            "type": "submit",
            "lay-filter": "login",
            "style": "width:100%;"
        }
    )


# 修改密码
class ResetPassword(FlaskForm):
    account = StringField(
        label='请输入旧密码',
        validators=[
            DataRequired()
        ],
        description="请输入旧密码",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入旧密码！",
            'autocomplete': 'off'
        }
    )
    pwd = PasswordField(
        label='请输入新密码',
        validators=[
            DataRequired()
        ],
        description="输入密码的输入框",
        render_kw={
            "type": "password",
            "class": "layui-input",
            "placeholder": "请输入新密码！",
            "lay-verify": "required",
            'autocomplete': 'off'
        }
    )
    repwd = PasswordField(
        label='请确认密码',
        validators=[
            DataRequired()
        ],
        description="确认密码的输入框",
        render_kw={
            "type": "password",
            "class": "layui-input",
            "placeholder": "请确认密码！",
            "lay-verify": "required",
            'autocomplete': 'off'
        }
    )
    submit = SubmitField(
        "修改密码",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
        }
    )


# 修改密码
class GuestForm(FlaskForm):
    id = None
    edit = False
    name = StringField(
        label='请输入客户姓名',
        validators=[
            DataRequired("姓名不能为空")
        ],
        description="请输入客户姓名",
        render_kw={
            "type": "text",
            "class": "layui-input",
            "placeholder": "请输入客户姓名",
            "required": False
        }
    )
    phone = StringField(
        label='请输入客户手机号',
        validators=[
            DataRequired("手机号不能为空")
        ],
        description="请输入客户手机号",
        render_kw={
            "type": "text",
            "class": "layui-input",
            "placeholder": "请输入客户手机号",
            "required": False
        }
    )
    email = StringField(
        label='请输入客户邮箱',
        description="请输入客户邮箱",
        render_kw={
            "type": "text",
            "class": "layui-input",
            "placeholder": "请输入客户邮箱",
        }
    )
    addr = StringField(
        label='请输入客户地区',
        description="请输入客户地区",
        render_kw={
            "type": "text",
            "class": "layui-input",
            "placeholder": "请输入客户地区",
        }
    )
    sex = SelectField(
        label="请选择性别",
        validators=[
            DataRequired()
        ],
        coerce=int,
        choices=[(1, "男"), (2, "女")],
        description="请选择性别",
        render_kw={
            "class": "contrller",
        }
    )
    submit = SubmitField(
        "保存",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
        }
    )

    def validate_name(self, field):
        name = field.data
        user = Guest.query.filter_by(user_name=name).count()
        if user == 1:
            raise ValidationError("昵称已存在")


# 客户管理查询
class GuestSearch(FlaskForm):
    name = StringField(
        description="客户名查询",
        render_kw={
            "type": "text",
            "placeholder": "客户名查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    phone = StringField(
        description="手机号查询",
        render_kw={
            "type": "text",
            "placeholder": "手机号查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    submit = SubmitField(
        "搜索",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
        }
    )


# 材质类型搜索
class GoodsTypeSearch(FlaskForm):
    name = StringField(
        description="类型名称",
        render_kw={
            "type": "text",
            "placeholder": "类型名称查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    submit = SubmitField(
        "搜索",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
        }
    )


# 材质类型
class GoodsTypeForm(FlaskForm):
    id = None
    name = StringField(
        label='请输入类型名称',
        validators=[
            DataRequired('用户名不能为空')
        ],
        description="请输入类型名称",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入类型名称",
        }
    )
    description = StringField(
        label='请输入类型描述',
        description="请输入类型描述",
        render_kw={
            "type": "text",
            "class": "layui-input",
            "placeholder": "请输入类型描述",
        }
    )
    submit = SubmitField(
        "保存",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
        }
    )

    def validate_name(self, field):
        name = field.data
        user = GoodsType.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError("商品类型存在")


# 材质类型搜索
class TypeItemSearch(FlaskForm):
    type_name = StringField(
        description="类型名称",
        render_kw={
            "type": "text",
            "placeholder": "类型名称查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )

    name = StringField(
        description="sku 名称",
        render_kw={
            "type": "text",
            "placeholder": "规格名称查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )

    description = TextAreaField(
        label='请输入类型描述',
        description="请输入类型描述",
        render_kw={
            "type": "text",
            "class": "layui-input",
            "placeholder": "请输入类型描述",
        }
    )

    submit = SubmitField(
        "搜索",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
        }
    )


# 材质类型
class TypeItemForm(FlaskForm):
    id = None
    good_types = GoodsType.query.filter(GoodsType.status == 1).all()
    type_name = SelectField(
        label="请选择类型",
        validators=[
            DataRequired()
        ],
        coerce=int,
        choices=[(i.id, i.name) for i in good_types],
        description="请选择类型",
        render_kw={
            "class": "contrller",
        }
    )

    name = StringField(
        label='类型规格',
        validators=[
            DataRequired()
        ],
        description="请输入类型规格",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入类型规格",
        }
    )

    unit = RadioField(
        label="请选择单位",
        validators=[
            DataRequired()
        ],
        coerce=int,
        choices=[(v, k) for k, v in UNIT.items()],
        description="请选择单位",
        render_kw={
            "class": "contrller",
        }
    )

    description = TextAreaField(
        label='请输入类型规格描述',
        description="请输入类型规格描述",
        render_kw={
            "type": "text",
            "class": "layui-input",
            "placeholder": "请输入类型规格描述",
        }
    )
    submit = SubmitField(
        "保存",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
        }
    )


# 订单明细
class DetailOrderForm(FlaskForm):
    types = GoodsType.query.filter(GoodsType.status == 1).all()
    type_items = TypeItem.query.filter(TypeItem.status == 1).all()

    type_id = SelectField(
        label="请选择类型",
        validators=[
            DataRequired()
        ],
        coerce=int,
        choices=[(i.id, i.name) for i in types],
        description="请选择类型",
        render_kw={
            "class": "contrller",
        }
    )

    item_id = SelectField(
        label="请选择类型",
        validators=[
            DataRequired()
        ],
        coerce=int,
        choices=[(i.id, i.item_name) for i in type_items],
        description="请选择类型",
        render_kw={
            "class": "contrller",
        }
    )
    price = IntegerField(
        label='单价',
        validators=[
            DataRequired()
        ],
        description="请输入单价",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入单价",
        }
    )
    num = IntegerField(
        label='数量',
        validators=[
            DataRequired()
        ],
        description="请输入数量",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入数量",
        }
    )

    unit = StringField(
        label='单位',
        validators=[
            DataRequired()
        ],
        description="请输入单位",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入单位",
        }
    )

    length = IntegerField(
        label='长度',
        validators=[
            DataRequired()
        ],
        description="请输入长度",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入长度",
        }
    )

    delete = SubmitField(
        "删除",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


# 订单
class OrderForm(FlaskForm):
    guests = Guest.query.filter(Guest.status == 1).all()
    guest_name = SelectField(
        label="选择客户",
        validators=[
            DataRequired()
        ],
        coerce=int,
        choices=[(0, '请选择')] + [(i.user_id, i.user_name) for i in guests],
        default=0,
        description="选择客户",
        render_kw={
            "class": "contrller",
        }
    )

    total = IntegerField(
        label='总价',
        validators=[
            DataRequired()
        ],
        description="请输入单位",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入单位",
        }
    )

    pay = IntegerField(
        label='已付款',
        validators=[
            DataRequired()
        ],
        description="请输入已付款金额",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入已付款金额",
        }
    )

    unpay = IntegerField(
        label='未付款',
        validators=[
            DataRequired()
        ],
        description="请输入未付款金额",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入未付款金额",
        }
    )

    description = TextAreaField(
        label='请输入描述',
        description="请输入描述",
        render_kw={
            "type": "text",
            "class": "layui-input",
            "placeholder": "请输入描述",
        },
        validators=[
            DataRequired()
        ],
    )

    details = FieldList(
        FormField(DetailOrderForm),
        min_entries=1,
        max_entries=20
    )

    submit = SubmitField(
        "保存",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


class OrderSearch(FlaskForm):
    order_no = StringField(
        description="订单号",
        render_kw={
            "type": "text",
            "placeholder": "订单号查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )

    name = StringField(
        description="客户姓名",
        render_kw={
            "type": "text",
            "placeholder": "客户姓名查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )

    submit = SubmitField(
        "搜索",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
        }
    )


class FinancialSearch(FlaskForm):
    phone = StringField(
        description="手机号",
        render_kw={
            "type": "text",
            "placeholder": "手机号查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )

    name = StringField(
        description="客户姓名",
        render_kw={
            "type": "text",
            "placeholder": "客户姓名查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )

    submit = SubmitField(
        "搜索",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
        }
    )
