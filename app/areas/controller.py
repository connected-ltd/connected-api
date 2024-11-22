from flask import Blueprint, request
from app.route_guard import auth_required

from app.areas.model import *
from app.areas.schema import *

bp = Blueprint('areas', __name__)

@bp.post('/areas')
@auth_required('super_admin')
def create_areas():
    name = request.json.get('name')
    areas = Areas.create(name)
    return {'data':AreasSchema().dump(areas), 'message': 'Areas created successfully', 'status':'success'}, 201

@bp.get('/areas/<int:id>')
@auth_required()
def get_areas(id):
    areas = Areas.get_by_id(id)
    if areas is None:
        return {'message': 'Areas not found'}, 404
    return {'data':AreasSchema().dump(areas), 'message': 'Areas fetched successfully', 'status':'success'}, 200

@bp.put('/areas/<int:id>')
@auth_required('super_admin')
def update_areas(id):
    areas = Areas.get_by_id(id)
    if areas is None:
        return {'message': 'Areas not found'}, 404
    name = request.json.get('name')
    areas.update(name)
    return {'data':AreasSchema().dump(areas), 'message': 'Areas updated successfully', 'status':'success'}, 200

@bp.patch('/areas/<int:id>')
@auth_required()
def patch_areas(id):
    areas = Areas.get_by_id(id)
    if areas is None:
        return {'message': 'Areas not found'}, 404
    name = request.json.get('name')
    areas.update(name)
    return {'data':AreasSchema().dump(areas), 'message': 'Areas updated successfully', 'status':'success'}, 200

@bp.delete('/areas/<int:id>')
@auth_required('super_admin')
def delete_areas(id):
    areas = Areas.get_by_id(id)
    if areas is None:
        return {'message': 'Areas not found'}, 404
    areas.delete()
    return {'message': 'Areas deleted successfully', 'status':'success'}, 200

@bp.get('/areas')
@auth_required()
def get_all_areas():
    areass = Areas.get_all()
    return {'data':AreasSchema(many=True).dump(areass), 'message': 'Areas fetched successfully', 'status':'success'}, 200

@bp.get('/areas/numbers')
# @auth_required()
def get_numbers_per_areas():
    areas_stats = Areas.get_numbers_per_area()
    return {'data':areas_stats, 'message': 'Numbers per Areas stats fetched successfully', 'status':'success'}, 200
