from flask import Blueprint, request
from app.route_guard import auth_required

from app.shortcodes.model import *
from app.shortcodes.schema import *

bp = Blueprint('shortcodes', __name__)

@bp.post('/shortcodes')
@auth_required()
def create_shortcodes():
    shortcode = request.json.get('shortcode')
    user_id = request.json.get('user_id')
    shortcodes = Shortcodes.create(shortcode, user_id)
    return {'data':ShortcodesSchema().dump(shortcodes), 'message': 'Shortcodes created successfully', 'status':'success'}, 201

@bp.get('/shortcodes/<int:id>')
@auth_required()
def get_shortcodes(id):
    shortcodes = Shortcodes.get_by_id(id)
    if shortcodes is None:
        return {'message': 'Shortcodes not found'}, 404
    return {'data':ShortcodesSchema().dump(shortcodes), 'message': 'Shortcodes fetched successfully', 'status':'success'}, 200

@bp.put('/shortcodes/<int:id>')
@auth_required()
def update_shortcodes(id):
    shortcodes = Shortcodes.get_by_id(id)
    if shortcodes is None:
        return {'message': 'Shortcodes not found'}, 404
    shortcode = request.json.get('shortcode')
    user_id = request.json.get('user_id')
    shortcodes.update(shortcode, user_id)
    return {'data':ShortcodesSchema().dump(shortcodes), 'message': 'Shortcodes updated successfully', 'status':'success'}, 200

@bp.patch('/shortcodes/<int:id>')
@auth_required()
def patch_shortcodes(id):
    shortcodes = Shortcodes.get_by_id(id)
    if shortcodes is None:
        return {'message': 'Shortcodes not found'}, 404
    shortcode = request.json.get('shortcode')
    user_id = request.json.get('user_id')
    shortcodes.update(shortcode, user_id)
    return {'data':ShortcodesSchema().dump(shortcodes), 'message': 'Shortcodes updated successfully', 'status':'success'}, 200

@bp.delete('/shortcodes/<int:id>')
@auth_required()
def delete_shortcodes(id):
    shortcodes = Shortcodes.get_by_id(id)
    if shortcodes is None:
        return {'message': 'Shortcodes not found'}, 404
    shortcodes.delete()
    return {'message': 'Shortcodes deleted successfully', 'status':'success'}, 200

@bp.get('/shortcodes')
@auth_required()
def get_all_shortcodes():
    shortcodess = Shortcodes.get_all()
    return {'data':ShortcodesSchema(many=True).dump(shortcodess), 'message': 'Shortcodes fetched successfully', 'status':'success'}, 200