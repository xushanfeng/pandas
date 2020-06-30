from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


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
    submit = SubmitField(
        "登录",
        render_kw={
            "type": "submit",
            "lay-filter": "login",
            "style": "width:100%;"
        }
    )
