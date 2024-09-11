from app import ma
from app.shortcodes.model import *

class ShortcodesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Shortcodes
        exclude = ('is_deleted',)