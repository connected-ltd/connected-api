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
from app.shortcode_files.model import *
# from helpers.langchain import train_with_resource
from app.celery.tasks import train_with_resource_in_background
from helpers.upload import do_upload

bp = Blueprint('files', __name__)

@bp.post('/files')
@auth_required()
def create_files():
    file = request.files.get('file')
    shortcode_data: Shortcodes = Shortcodes.get_by_user_id(g.user.id)
    shortcode = ShortcodesSchema().dump(shortcode_data)
    if file:
        resource_url = do_upload(file)
        train_with_resource_in_background.delay(resource_url, shortcode['shortcode'])
        # train_with_resource(resource_url, shortcode['shortcode'])
        print("File name: ", file.filename)
        print("User id: ", g.user.id)
        fileData = Files.create(file.filename, g.user.id)
        return {'data':FilesSchema().dump(fileData), 'message': 'Files created successfully', 'status':'success'}, 201
    return {'message': 'No file was supplied', 'status':'failed'}, 500

    

@bp.post('/files/whatsapp')
@auth_required()
def create_whatsapp_files():
    file = request.files.get('file')
    whatsapp_number_data: Whatsapp_Number = Whatsapp_Number.get_by_user_id(g.user.id)
    whatsapp_number = Whatsapp_NumberSchema().dump(whatsapp_number_data)
    formatted_whatsapp_number = whatsapp_number['number'].split('+')[1].strip()
    if file:
        resource_url = do_upload(file)
        train_with_resource_in_background.delay(resource_url, formatted_whatsapp_number)
        # train_with_resource(resource_url, shortcode['shortcode'])
        print("File name: ", file.filename)
        print("User id: ", g.user.id)
        fileData = Files.create(file.filename, g.user.id)
        return {'data':FilesSchema().dump(fileData), 'message': 'Files created successfully', 'status':'success'}, 201
    return {'message': 'No file was supplied', 'status':'failed'}, 500
# TODO: Test this endpoint later
        

# @bp.post('/files')
# @auth_required()
# def create_files():
#     file = request.files.get('file')
#     user_id = request.form.get('user_id')
#     shortcode = request.form.get('shortcode')
#     username = User.get_username_by_id(user_id)
#     user_classname = username.split('@')[0].replace('-', '_').replace('.', '_').replace(',', '_')
#     if file:
#         if not (file.filename.lower().endswith('.pdf') or file.filename.lower().endswith('.docx')):
#             return {'message':'Only PDf and DOCX files are allowed'}, 400
        
#         wv_class_name = f"{user_classname}_{file.filename.split('.')[0]}".replace(" ", "").replace("-", "")
        
#         result, status_code = process_uploaded_file(file, wv_client, wv_class_name)  

#         if result['status'] == "exists":
#             return result, status_code
#         elif result['status'] == "error":
#             return result, status_code
#         print(result, status_code)
        
#         try:     
#             # TODO: Handle when file already exists
#             added_file = Files.create(file.filename, user_id, wv_class_name)
            
#             if added_file:    
#                 # TODO: Handle when shortcode already exists
#                 added_shortcode = Shortcodes.create(shortcode, user_id) 
#                 if added_shortcode:
#                     file_id = added_file.id
#                     Shortcode_Files.create(added_shortcode.id, file_id)
                    
#         except:
#             wv_delete_doc(wv_client, wv_class_name, file.filename)
#             return {'message': 'Error uploading file', 'status': 'error'}, 500
#         finally:
#             wv_client.close()
        
#         wv_client.close()        
#         return {'data':FilesSchema().dump(file), 'message': 'Files created successfully', 'status':'success'}, 201
#     else:
#         return {'message':'No file was provided'}, 500

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
    filess = Files.get_all()
    return {'data':FilesSchema(many=True).dump(filess), 'message': 'Files fetched successfully', 'status':'success'}, 200