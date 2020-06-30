from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import Guest


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
    #
    # def validate_name(self, field):
    #     name = field.data
    #     user = Guest.query.filter_by(user_name=name).count()
    #     if user == 1:
    #         raise ValidationError("昵称已存在")


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
