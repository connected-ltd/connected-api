from flask import Blueprint, request
from app.route_guard import auth_required

from app.numbers.model import *
from app.numbers.schema import *

bp = Blueprint('numbers', __name__)

@bp.post('/numbers')
@auth_required('admin', 'super_admin')
def create_numbers():
    number = request.json.get('number')
    language = request.json.get('language') 
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
    return {'data':[stats], 'message': 'Numbers statistics fetched successfully', 'status':'success'}, 200

# @bp.patch('/numbers/bulk-set-all')
# @auth_required('admin', 'super_admin')
# def bulk_set_all_numbers():
#     # Get all existing numbers
#     numbers = Numbers.get_all()
    
#     if not numbers:
#         return {'message': 'No numbers found', 'status': 'error'}, 404

#     # Bulk update all numbers
#     for number in numbers:
#         number.update(is_set=True)

#     return {
#         'data': NumbersSchema(many=True).dump(numbers), 
#         'message': f'{len(numbers)} numbers set status updated successfully', 
#         'status': 'success'
#     }, 200