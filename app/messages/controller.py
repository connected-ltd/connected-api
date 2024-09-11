from flask import Blueprint, request
from app.route_guard import auth_required

from app.messages.model import *
from app.messages.schema import *

bp = Blueprint('messages', __name__)

@bp.post('/messages')
@auth_required()
def create_messages():
    content = request.json.get('content')
    shortcode_id = request.json.get('shortcode_id')
    user_id = request.json.get('user_id')
    areas = request.json.get('areas')
    messages = Messages.create(content, shortcode_id, user_id, areas)
    return {'data':MessagesSchema().dump(messages), 'message': 'Messages created successfully', 'status':'success'}, 201

@bp.get('/messages/<int:id>')
@auth_required()
def get_messages(id):
    messages = Messages.get_by_id(id)
    if messages is None:
        return {'message': 'Messages not found'}, 404
    return {'data':MessagesSchema().dump(messages), 'message': 'Messages fetched successfully', 'status':'success'}, 200

@bp.put('/messages/<int:id>')
@auth_required()
def update_messages(id):
    messages = Messages.get_by_id(id)
    if messages is None:
        return {'message': 'Messages not found'}, 404
    content = request.json.get('content')
    shortcode_id = request.json.get('shortcode_id')
    user_id = request.json.get('user_id')
    areas = request.json.get('areas')
    messages.update(content, shortcode_id, user_id, areas)
    return {'data':MessagesSchema().dump(messages), 'message': 'Messages updated successfully', 'status':'success'}, 200

@bp.patch('/messages/<int:id>')
@auth_required()
def patch_messages(id):
    messages = Messages.get_by_id(id)
    if messages is None:
        return {'message': 'Messages not found'}, 404
    content = request.json.get('content')
    shortcode_id = request.json.get('shortcode_id')
    user_id = request.json.get('user_id')
    areas = request.json.get('areas')
    messages.update(content, shortcode_id, user_id, areas)
    return {'data':MessagesSchema().dump(messages), 'message': 'Messages updated successfully', 'status':'success'}, 200

@bp.delete('/messages/<int:id>')
@auth_required()
def delete_messages(id):
    messages = Messages.get_by_id(id)
    if messages is None:
        return {'message': 'Messages not found'}, 404
    messages.delete()
    return {'message': 'Messages deleted successfully', 'status':'success'}, 200

@bp.get('/messages')
@auth_required()
def get_all_messages():
    messagess = Messages.get_all()
    return {'data':MessagesSchema(many=True).dump(messagess), 'message': 'Messages fetched successfully', 'status':'success'}, 200