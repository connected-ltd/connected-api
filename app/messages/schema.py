from app import ma
from app.messages.model import *

class MessagesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Messages
        exclude = ('is_deleted',)