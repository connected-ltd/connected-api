from flask import Blueprint, request
from app.route_guard import auth_required

from app.messages.model import *
from app.messages.schema import *
from app.numbers.model import *
from app.shortcodes.model import *
from helpers.africastalking import AfricasTalking

bp = Blueprint('messages', __name__)

@bp.post('/messages')
@auth_required()
def create_messages():
    message = request.json.get('message')
    shortcode_id = request.json.get('shortcode_id')
    user_id = request.json.get('user_id')
    area_id = request.json.get('area_id')
    numbers_to_send = Numbers.get_all_numbers_only_by_area_id(area_id)
    sender_shortcode = Shortcodes.get_shortcode_only_by_id(shortcode_id)
    for number in numbers_to_send:
        response = AfricasTalking().send(sender=sender_shortcode, message=message, recipients=number)
        if response["SMSMessageData"]["Recipients"][0]["statusCode"] == 101: 
            messages = Messages.create(message, shortcode_id, user_id, area_id)
            return {'data':MessagesSchema().dump(messages), 'message': 'Messages created successfully', 'status':'success'}, 201
        else:
            return {'message':'Please make sure parameters are valid!'}, 400

@bp.post('/messages/reply')
# @auth_required
def respond_to_message():
    response = request.form
    print(f"message: {response.get('text')}")
    print(f"from: {response.get('from')}")
    print(f"to: {response.get('to')}")
    
    return response
    

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
    message = request.json.get('message')
    shortcode_id = request.json.get('shortcode_id')
    user_id = request.json.get('user_id')
    area_id = request.json.get('area_id')
    messages.update(message, shortcode_id, user_id, area_id)
    return {'data':MessagesSchema().dump(messages), 'message': 'Messages updated successfully', 'status':'success'}, 200

@bp.patch('/messages/<int:id>')
@auth_required()
def patch_messages(id):
    messages = Messages.get_by_id(id)
    if messages is None:
        return {'message': 'Messages not found'}, 404
    message = request.json.get('message')
    shortcode_id = request.json.get('shortcode_id')
    user_id = request.json.get('user_id')
    area_id = request.json.get('area_id')
    messages.update(message, shortcode_id, user_id, area_id)
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