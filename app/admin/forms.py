# 登陆表单
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FieldList, FormField, \
    IntegerField
from wtforms.validators import DataRequired

from app.models import GoodsType, Guest


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
            "style": "width:100%;",
            "onclick": "mesg()"
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
    name = StringField(
        label='请输入客户姓名',
        validators=[
            DataRequired()
        ],
        description="请输入客户姓名",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入客户姓名",
        }
    )
    email = PasswordField(
        label='请输入客户邮箱',
        validators=[
            DataRequired()
        ],
        description="请输入客户邮箱",
        render_kw={
            "type": "text",
            "class": "layui-input",
            "placeholder": "请输入客户邮箱",
            "lay-verify": "required",
        }
    )
    phone = PasswordField(
        label='请输入客户手机号',
        validators=[
            DataRequired()
        ],
        description="请输入客户手机号",
        render_kw={
            "type": "text",
            "class": "layui-input",
            "placeholder": "请输入客户手机号",
            "lay-verify": "required",
        }
    )
    sex = SelectField(
        label="请选择性别",
        validators=[
            DataRequired()
        ],
        coerce=int,
        choices=[(0, "性别"), (1, "男"), (2, "女")],
        description="请选择性别",

        render_kw={
            "class": "contrller",
        }
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


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
            "onclick": "mesg()"
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
            "onclick": "mesg()"
        }
    )


# 材质类型
class GoodsTypeForm(FlaskForm):
    name = StringField(
        label='请输入客户姓名',
        validators=[
            DataRequired()
        ],
        description="请输入客户姓名",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入客户姓名",
        }
    )
    description = PasswordField(
        label='请输入类型描述',
        validators=[
            DataRequired()
        ],
        description="请输入类型描述",
        render_kw={
            "type": "text",
            "class": "layui-input",
            "placeholder": "请输入类型描述",
        }
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


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
            "placeholder": "类型名称查询",
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
            "onclick": "mesg()"
        }
    )


# 材质类型
class TypeItemForm(FlaskForm):
    good_types = GoodsType.query.all()
    print(good_types)
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
        "添加",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


# 订单明细
class DetailOrderForm(FlaskForm):
    type_name = SelectField()
    type_item_name = SelectField()
    price = StringField(
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
    num = StringField(
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


# 订单
class OrderForm(FlaskForm):
    guests = Guest.query.all()
    guest_name = SelectField(
        label="选择客户",
        validators=[
            DataRequired()
        ],
        coerce=int,
        choices=[(i.user_id, i.user_name) for i in guests],
        description="选择客户",
        render_kw={
            "class": "contrller",
        }
    )

    description = TextAreaField(
        label='请输入描述',
        description="请输入描述",
        render_kw={
            "type": "text",
            "class": "layui-input",
            "placeholder": "请输入描述",
        }
    )

    details = FieldList(
        FormField(DetailOrderForm),
        min_entries=1,
        max_entries=20
    )

    submit = SubmitField(
        "添加",
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
            "onclick": "mesg()"
        }
    )
