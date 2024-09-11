from app import ma
from app.areas.model import *

class AreasSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Areas
        exclude = ('is_deleted',)