from wtforms import StringField, validators, IntegerField
from .our_form import OurForm


class TagForm(OurForm):
    category = StringField("category", [validators.Length(min=1, max=30)])
    tag_name = StringField("tag_name", [validators.Length(min=1, max=50)])


class StockTagForm(OurForm):
    stock_id = IntegerField("stock_id", [validators.required()])
    tag_name = StringField("tag_name", [validators.Length(min=1, max=50), validators.required()])
    category = StringField("category", [validators.Length(min=1, max=50), validators.required()])
