from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


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
    name = StringField(
        label='请输入类型名称',
        validators=[
            DataRequired()
        ],
        description="请输入类型名称",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入类型名称",
            "required": False
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
