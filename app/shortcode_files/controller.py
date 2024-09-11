from flask import Blueprint, request
from app.route_guard import auth_required

from app.shortcode_files.model import *
from app.shortcode_files.schema import *

bp = Blueprint('shortcode_files', __name__)

@bp.post('/shortcode_files')
@auth_required()
def create_shortcode_files():
    shortcode_id = request.json.get('shortcode_id')
    file_id = request.json.get('file_id')
    shortcode_files = Shortcode_Files.create(shortcode_id, file_id)
    return {'data':Shortcode_FilesSchema().dump(shortcode_files), 'message': 'Shortcode_Files created successfully', 'status':'success'}, 201

@bp.get('/shortcode_files/<int:id>')
@auth_required()
def get_shortcode_files(id):
    shortcode_files = Shortcode_Files.get_by_id(id)
    if shortcode_files is None:
        return {'message': 'Shortcode_Files not found'}, 404
    return {'data':Shortcode_FilesSchema().dump(shortcode_files), 'message': 'Shortcode_Files fetched successfully', 'status':'success'}, 200

@bp.put('/shortcode_files/<int:id>')
@auth_required()
def update_shortcode_files(id):
    shortcode_files = Shortcode_Files.get_by_id(id)
    if shortcode_files is None:
        return {'message': 'Shortcode_Files not found'}, 404
    shortcode_id = request.json.get('shortcode_id')
    file_id = request.json.get('file_id')
    shortcode_files.update(shortcode_id, file_id)
    return {'data':Shortcode_FilesSchema().dump(shortcode_files), 'message': 'Shortcode_Files updated successfully', 'status':'success'}, 200

@bp.patch('/shortcode_files/<int:id>')
@auth_required()
def patch_shortcode_files(id):
    shortcode_files = Shortcode_Files.get_by_id(id)
    if shortcode_files is None:
        return {'message': 'Shortcode_Files not found'}, 404
    shortcode_id = request.json.get('shortcode_id')
    file_id = request.json.get('file_id')
    shortcode_files.update(shortcode_id, file_id)
    return {'data':Shortcode_FilesSchema().dump(shortcode_files), 'message': 'Shortcode_Files updated successfully', 'status':'success'}, 200

@bp.delete('/shortcode_files/<int:id>')
@auth_required()
def delete_shortcode_files(id):
    shortcode_files = Shortcode_Files.get_by_id(id)
    if shortcode_files is None:
        return {'message': 'Shortcode_Files not found'}, 404
    shortcode_files.delete()
    return {'message': 'Shortcode_Files deleted successfully', 'status':'success'}, 200

@bp.get('/shortcode_files')
@auth_required()
def get_all_shortcode_files():
    shortcode_filess = Shortcode_Files.get_all()
    return {'data':Shortcode_FilesSchema(many=True).dump(shortcode_filess), 'message': 'Shortcode_Files fetched successfully', 'status':'success'}, 200