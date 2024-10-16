from flask import Blueprint, request
from app.route_guard import auth_required

from app.numbers.model import *
from app.numbers.schema import *

bp = Blueprint('numbers', __name__)

@bp.post('/numbers')
@auth_required('admin', 'super_admin')
def create_numbers():
    number = request.json.get('number')
    language = request.json.get('language') # TODO: Make the language selection a dropdown instead to avoid disparities on the database
    area_id = request.json.get('area_id')
    if number[0:4] == "+234" and len(number) == 14:
        numbers = Numbers.create(number, language, area_id)
        return {'data':NumbersSchema().dump(numbers), 'message': 'Numbers created successfully', 'status':'success'}, 201
    elif number[0:4] == "+234" and len(number) != 14:
        return {'message':'Number is invalid! Please try again'}, 400
    else:
        return {'message':'Number format is wrong! Please make sure the number starts with +234'}, 400

@bp.get('/numbers/<int:id>')
@auth_required('admin', 'super_admin')
def get_numbers(id):
    numbers = Numbers.get_by_id(id)
    if numbers is None:
        return {'message': 'Numbers not found'}, 404
    return {'data':NumbersSchema().dump(numbers), 'message': 'Numbers fetched successfully', 'status':'success'}, 200

@bp.put('/numbers/<int:id>')
@auth_required('admin', 'super_admin')
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
@auth_required('admin', 'super_admin')
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
@auth_required('admin', 'super_admin')
def delete_numbers(id):
    numbers = Numbers.get_by_id(id)
    if numbers is None:
        return {'message': 'Numbers not found'}, 404
    numbers.delete()
    return {'message': 'Numbers deleted successfully', 'status':'success'}, 200

@bp.get('/numbers')
@auth_required('admin', 'super_admin')
def get_all_numbers():
    numberss = Numbers.get_all()
    return {'data':NumbersSchema(many=True).dump(numberss), 'message': 'Numbers fetched successfully', 'status':'success'}, 200

@bp.get('/numbers/stats')
@auth_required('admin', 'super_admin')
def get_numbers_stats():
    stats = Numbers.get_numbers_stats()
    formatted_stats = [{"language": lang, "count": count} for lang, count in stats.items()]
    return {'data':formatted_stats, 'message': 'Numbers statistics fetched successfully', 'status':'success'}, 200