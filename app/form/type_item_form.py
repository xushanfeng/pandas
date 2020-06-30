from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, RadioField
from wtforms.validators import DataRequired

from app.constant.const import UNIT
from app.models import GoodsType


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
