from flask import Blueprint, request
from app.route_guard import auth_required

from app.numbers.model import *
from app.numbers.schema import *

bp = Blueprint('numbers', __name__)

@bp.post('/numbers')
@auth_required()
def create_numbers():
    number = request.json.get('number')
    language = request.json.get('language')
    area_id = request.json.get('area_id')
    numbers = Numbers.create(number, language, area_id)
    return {'data':NumbersSchema().dump(numbers), 'message': 'Numbers created successfully', 'status':'success'}, 201

@bp.get('/numbers/<int:id>')
@auth_required()
def get_numbers(id):
    numbers = Numbers.get_by_id(id)
    if numbers is None:
        return {'message': 'Numbers not found'}, 404
    return {'data':NumbersSchema().dump(numbers), 'message': 'Numbers fetched successfully', 'status':'success'}, 200

@bp.put('/numbers/<int:id>')
@auth_required()
def update_numbers(id):
    numbers = Numbers.get_by_id(id)
    if numbers is None:
        return {'message': 'Numbers not found'}, 404
    number = request.json.get('number')
    language = request.json.get('language')
    area_id = request.json.get('area_id')
    numbers.update(number, language, area_id)
    return {'data':NumbersSchema().dump(numbers), 'message': 'Numbers updated successfully', 'status':'success'}, 200

@bp.patch('/numbers/<int:id>')
@auth_required()
def patch_numbers(id):
    numbers = Numbers.get_by_id(id)
    if numbers is None:
        return {'message': 'Numbers not found'}, 404
    number = request.json.get('number')
    language = request.json.get('language')
    area_id = request.json.get('area_id')
    numbers.update(number, language, area_id)
    return {'data':NumbersSchema().dump(numbers), 'message': 'Numbers updated successfully', 'status':'success'}, 200

@bp.delete('/numbers/<int:id>')
@auth_required()
def delete_numbers(id):
    numbers = Numbers.get_by_id(id)
    if numbers is None:
        return {'message': 'Numbers not found'}, 404
    numbers.delete()
    return {'message': 'Numbers deleted successfully', 'status':'success'}, 200

@bp.get('/numbers')
@auth_required()
def get_all_numbers():
    numberss = Numbers.get_all()
    return {'data':NumbersSchema(many=True).dump(numberss), 'message': 'Numbers fetched successfully', 'status':'success'}, 200