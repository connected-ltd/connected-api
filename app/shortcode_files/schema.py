from app import ma
from app.shortcode_files.model import *

class Shortcode_FilesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Shortcode_Files
        exclude = ('is_deleted',)