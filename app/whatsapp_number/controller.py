from flask import Blueprint, request
from app.route_guard import auth_required

from app.whatsapp_number.model import *
from app.whatsapp_number.schema import *

bp = Blueprint('whatsapp_number', __name__)

@bp.post('/whatsapp_number')
@auth_required()
def create_whatsapp_number():
    number = request.json.get('number')
    user_id = request.json.get('user_id')
    whatsapp_number = Whatsapp_Number.create(number, user_id)
    return {'data':Whatsapp_NumberSchema().dump(whatsapp_number), 'message': 'Whatsapp_Number created successfully', 'status':'success'}, 201

@bp.get('/whatsapp_number/<int:id>')
@auth_required()
def get_whatsapp_number(id):
    whatsapp_number = Whatsapp_Number.get_by_id(id)
    if whatsapp_number is None:
        return {'message': 'Whatsapp_Number not found'}, 404
    return {'data':Whatsapp_NumberSchema().dump(whatsapp_number), 'message': 'Whatsapp_Number fetched successfully', 'status':'success'}, 200

@bp.put('/whatsapp_number/<int:id>')
@auth_required()
def update_whatsapp_number(id):
    whatsapp_number = Whatsapp_Number.get_by_id(id)
    if whatsapp_number is None:
        return {'message': 'Whatsapp_Number not found'}, 404
    number = request.json.get('number')
    user_id = request.json.get('user_id')
    whatsapp_number.update(number, user_id)
    return {'data':Whatsapp_NumberSchema().dump(whatsapp_number), 'message': 'Whatsapp_Number updated successfully', 'status':'success'}, 200

@bp.patch('/whatsapp_number/<int:id>')
@auth_required()
def patch_whatsapp_number(id):
    whatsapp_number = Whatsapp_Number.get_by_id(id)
    if whatsapp_number is None:
        return {'message': 'Whatsapp_Number not found'}, 404
    number = request.json.get('number')
    user_id = request.json.get('user_id')
    whatsapp_number.update(number, user_id)
    return {'data':Whatsapp_NumberSchema().dump(whatsapp_number), 'message': 'Whatsapp_Number updated successfully', 'status':'success'}, 200

@bp.delete('/whatsapp_number/<int:id>')
@auth_required()
def delete_whatsapp_number(id):
    whatsapp_number = Whatsapp_Number.get_by_id(id)
    if whatsapp_number is None:
        return {'message': 'Whatsapp_Number not found'}, 404
    whatsapp_number.delete()
    return {'message': 'Whatsapp_Number deleted successfully', 'status':'success'}, 200

@bp.get('/whatsapp_number')
@auth_required()
def get_all_whatsapp_number():
    whatsapp_numbers = Whatsapp_Number.get_all()
    return {'data':Whatsapp_NumberSchema(many=True).dump(whatsapp_numbers), 'message': 'Whatsapp_Number fetched successfully', 'status':'success'}, 200