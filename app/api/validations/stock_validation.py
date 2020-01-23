from wtforms import StringField, FormField, FieldList, validators
from .our_form import OurForm


class StockForm(OurForm):
    ticker = StringField('ticker', [validators.Length(min=1, max=50),
                                    validators.DataRequired()])
    stock_name = StringField('stock_name', [validators.Length(min=1, max=200),
                                            validators.DataRequired()])
    exchange = StringField('exchange', [validators.Length(min=1, max=10),
                                        validators.DataRequired()])


class StocksForm(OurForm):
    stocks = FieldList(FormField(StockForm))


class TickersForm(OurForm):
    stocks = FieldList(StringField('ticker'))
