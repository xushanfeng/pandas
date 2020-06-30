from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


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