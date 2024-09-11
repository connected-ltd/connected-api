from app import ma
from app.files.model import *

class FilesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Files
        exclude = ('is_deleted',)