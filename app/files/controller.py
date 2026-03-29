from flask import Blueprint, request, g
from app.route_guard import auth_required

from app.files.model import *
from app.files.schema import *
from app.user.model import *
from app.user.schema import *
from app.shortcodes.model import *
from app.shortcodes.schema import *
from app.whatsapp_number.model import *
from app.whatsapp_number.schema import *
# from helpers.langchain import train_with_resource
from app.celery.tasks import train_with_resource_in_background
from helpers.upload import do_upload

bp = Blueprint('files', __name__)

@bp.post('/files')
@auth_required()
def create_files():
    file = request.files.get('file')
    shortcode_data = Shortcodes.get_by_user_id(g.user.id)
    
    if not file:
        return {'message': 'No file supplied', 'status': 'failed'}, 400
    if not shortcode_data:
        return {'message': 'Shortcode not found', 'status': 'failed'}, 404

    resource_url = do_upload(file)
    
    train_with_resource_in_background.delay(
        resource_url=resource_url,
        filename=file.filename,
        user_id=g.user.id,
        index_identifier=shortcode_data.shortcode,
        shortcode_id=shortcode_data.id
    )
    
    return {'message': 'File is being processed. It will be available shortly.', 'status': 'processing'}, 202


@bp.post('/files/whatsapp')
@auth_required()
def create_whatsapp_files():
    file = request.files.get('file')
    whatsapp_data = Whatsapp_Number.get_by_user_id(g.user.id)
    
    if not file:
        return {'message': 'No file supplied', 'status': 'failed'}, 400
    if not whatsapp_data:
        return {'message': 'WhatsApp number not found', 'status': 'failed'}, 404

    formatted_number = whatsapp_data.number.split('+')[1].strip()
    resource_url = do_upload(file)
    
    # Pass whatsapp_number_id, leave shortcode_id as None
    train_with_resource_in_background.delay(
        resource_url=resource_url,
        filename=file.filename,
        user_id=g.user.id,
        index_identifier=formatted_number,
        whatsapp_number_id=whatsapp_data.id
    )
    
    return {'message': 'WhatsApp file is being processed.', 'status': 'processing'}, 202

        

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
    files.update(name, user_id)
    return {'data':FilesSchema().dump(files), 'message': 'Files updated successfully', 'status':'success'}, 200

@bp.patch('/files/<int:id>')
@auth_required()
def patch_files(id):
    files = Files.get_by_id(id)
    if files is None:
        return {'message': 'Files not found'}, 404
    name = request.json.get('name')
    user_id = request.json.get('user_id')
    files.update(name, user_id)
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
    data = Files.get_all_with_shortcodes_and_whatsapp()
    return {'data': data, 'message': 'Files fetched successfully', 'status': 'success'}, 200