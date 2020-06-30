from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField


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

    start_time = DateTimeField('开始时间',
                               format='%Y-%m-%d',
                               render_kw={
                                   "type": "text",
                                   "autocomplete": "off",
                                   "class": "layui-input",
                                   "id": "start_time",
                                   "placeholder": "开始时间"
                               }
                               )
    end_time = DateTimeField('结束时间',
                             format='%Y-%m-%d',
                             render_kw={
                                 "type": "text",
                                 "autocomplete": "off",
                                 "class": "layui-input",
                                 "id": "end_time",
                                 "placeholder": "结束时间"
                             }
                             )

    submit = SubmitField(
        "搜索",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
        }
    )