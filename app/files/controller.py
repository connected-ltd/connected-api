from flask import Blueprint, request
from app.route_guard import auth_required

from app.files.model import *
from app.files.schema import *

bp = Blueprint('files', __name__)

@bp.post('/files')
@auth_required()
def create_files():
    name = request.json.get('name')
    user_id = request.json.get('user_id')
    weaviate_class = request.json.get('weaviate_class')
    files = Files.create(name, user_id, weaviate_class)
    return {'data':FilesSchema().dump(files), 'message': 'Files created successfully', 'status':'success'}, 201

@bp.get('/files/<int:id>')
@auth_required()
def get_files(id):
    files = Files.get_by_id(id)
    if files is None:
        return {'message': 'Files not found'}, 404
    return {'data':FilesSchema().dump(files), 'message': 'Files fetched successfully', 'status':'success'}, 200

@bp.put('/files/<int:id>')
@auth_required()
def update_files(id):
    files = Files.get_by_id(id)
    if files is None:
        return {'message': 'Files not found'}, 404
    name = request.json.get('name')
    user_id = request.json.get('user_id')
    weaviate_class = request.json.get('weaviate_class')
    files.update(name, user_id, weaviate_class)
    return {'data':FilesSchema().dump(files), 'message': 'Files updated successfully', 'status':'success'}, 200

@bp.patch('/files/<int:id>')
@auth_required()
def patch_files(id):
    files = Files.get_by_id(id)
    if files is None:
        return {'message': 'Files not found'}, 404
    name = request.json.get('name')
    user_id = request.json.get('user_id')
    weaviate_class = request.json.get('weaviate_class')
    files.update(name, user_id, weaviate_class)
    return {'data':FilesSchema().dump(files), 'message': 'Files updated successfully', 'status':'success'}, 200

@bp.delete('/files/<int:id>')
@auth_required()
def delete_files(id):
    files = Files.get_by_id(id)
    if files is None:
        return {'message': 'Files not found'}, 404
    files.delete()
    return {'message': 'Files deleted successfully', 'status':'success'}, 200

@bp.get('/files')
@auth_required()
def get_all_files():
    filess = Files.get_all()
    return {'data':FilesSchema(many=True).dump(filess), 'message': 'Files fetched successfully', 'status':'success'}, 200