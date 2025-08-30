from app import ma
from app.numbers.model import *


class NumbersSchema(ma.SQLAlchemyAutoSchema):
    area = ma.Function(lambda obj: obj.area.name if obj.area else None)
    class Meta:
        model = Numbers
        exclude = ('is_deleted', 'area_id')