from app import ma
from app.numbers.model import *

class NumbersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Numbers
        exclude = ('is_deleted',)