from app import ma
from app.whatsapp_number.model import *

class Whatsapp_NumberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Whatsapp_Number
        exclude = ('is_deleted',)
    