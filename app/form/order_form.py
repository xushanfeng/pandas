import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, FieldList, FormField, \
    IntegerField, DateField, DateTimeField
from wtforms.validators import DataRequired
from app.models import GoodsType, Guest, TypeItem


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
