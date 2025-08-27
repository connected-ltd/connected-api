from flask import Blueprint, request
from app.route_guard import auth_required

from app.messages.model import *
from app.messages.schema import *
from app.numbers.schema import *
from app.numbers.model import *
from app.shortcodes.model import *
from app.files.model import *
from helpers.africastalking import AfricasTalking
from helpers.twilio import send_twilio_message
from helpers.langchain import qa_chain

bp = Blueprint('messages', __name__)

@bp.post('/broadcast')
@auth_required()
def create_messages():
    message = request.json.get('message')
    shortcode_id = request.json.get('shortcode_id')
    user_id = request.json.get('user_id')
    area_id = request.json.get('area_id')
    numbers_to_send = Numbers.get_all_numbers_only_by_area_id(area_id)
    sender_shortcode = Shortcodes.get_shortcode_only_by_id(shortcode_id)
    if numbers_to_send:
        for number in numbers_to_send:
            response = AfricasTalking().send(sender=sender_shortcode, message=message, recipients=number)
            if response["SMSMessageData"]["Recipients"][0]["statusCode"] == 101: 
                messages = Messages.create(message, shortcode_id, user_id, area_id)
                return {'data':MessagesSchema().dump(messages), 'message': 'Messages created successfully', 'status':'success'}, 201
            else:
                return {'message':'Please make sure parameters are valid!'}, 400
    else:
        return {'message':'No numbers exist currently in this area'}

@bp.post('/messages/reply')
def respond_to_message():
    response = request.form
    chat_history = []
    sender_number = response.get('from')
    shortcode = response.get('to')
    message = response.get('text')
    
    appended_message = f'{message}'
        
    number_exists = Numbers.check_if_number_exists(sender_number)
    user_language = Numbers.get_language_by_number(sender_number)
    # print("Language: ", user_language)
    if number_exists:
        answer = qa_chain(appended_message, chat_history, shortcode, user_language)
        AfricasTalking().send(sender=shortcode, message=answer, recipients=[sender_number])
    else:
        AfricasTalking().send(sender=shortcode, message="Your number is not registered in our system, please dial *347*875# to register.", recipients=[sender_number])    
    
    
    return response

@bp.post('/messages/twilio')
def twilio_response():
    try:
        response = request.form
        chat_history = []
        sender_number = response.get('From')  
        recipient_number = response.get('To')
        message = response.get('Body')
 
        
        appended_message = f'{message}'
        
        formatted_sender_number = sender_number.split(':')[1].strip()
        formatted_recipient_number = recipient_number.split('+')[1].strip()
        
        number_exists = Numbers.check_if_number_exists(formatted_sender_number)
        user_language = Numbers.get_language_by_number(formatted_sender_number)
        if number_exists:
            answer = qa_chain(appended_message, chat_history, formatted_recipient_number, user_language)
            send_twilio_message(to=sender_number, message=answer, from_=recipient_number)
        else:
            send_twilio_message(to=sender_number, message="Your number is not registered in our system, please dial *347*875# to register.", from_=recipient_number)    
        
        
        return response

        # response_body = send_twilio_message(from_=recipient_number, to=sender_number)


        # return {"message": "Message sent successfully", "response_body": response_body}, 200
    except Exception as e:
        print(f"Error: {e}")
        return {"message": f"Failed to send message: {str(e)}"}, 500
    
    
@bp.post('/messages/twilio/sms')
def twilio_sms_response():
    try:
        response = request.form
        chat_history = []
        sender_number = response.get('From')  
        recipient_number = response.get('To')
        message = response.get('Body')
        print()
 
        
        appended_message = f'{message}'
        
        # formatted_sender_number = sender_number.split(':')[1].strip()
        formatted_recipient_number = recipient_number.split('+')[1].strip()
        
        number_exists = Numbers.check_if_number_exists(sender_number)
        user_language = Numbers.get_language_by_number(sender_number)
        if number_exists:
            answer = qa_chain(appended_message, chat_history, formatted_recipient_number, user_language)
            send_twilio_message(to=sender_number, message=answer, from_=recipient_number)
        else:
            send_twilio_message(to=sender_number, message="Your number is not registered in our system, please dial *347*875# to register.", from_=recipient_number)    
        
        
        return message

        # response_body = send_twilio_message(from_=recipient_number, to=sender_number)


        # return {"message": "Message sent successfully", "response_body": response_body}, 200
    except Exception as e:
        print(f"Error: {e}")
        return {"message": f"Failed to send message: {str(e)}"}, 500
    
    

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