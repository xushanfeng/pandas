from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


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
