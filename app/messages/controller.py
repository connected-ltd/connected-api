from flask import Blueprint, request, current_app
from app.route_guard import auth_required
from flask_jwt_extended import get_jwt_identity
from datetime import datetime

from app.messages.model import *
from app.messages.schema import *
from app.numbers.schema import *
from app.numbers.model import *
from app.shortcodes.model import *
from app.files.model import *
from app.credit.model import CreditPoints, CreditUsage, CreditTransaction
from app.credit.schema import CreditUsageSchema
from helpers.africastalking import AfricasTalking
from helpers.twilio import send_twilio_message
from helpers.langchain import qa_chain

bp = Blueprint('messages', __name__)

# Cost per message in credits
BROADCAST_CREDIT_COST = 0.5
RESPONSE_CREDIT_COST = 1
@bp.post('/broadcast')
@auth_required()
def create_messages():
    try:
        message = request.json.get('message')
        shortcode_id = request.json.get('shortcode_id')
        user_id = request.json.get('user_id')
        area_id = request.json.get('area_id')
        
        # Get numbers and validate shortcode
        numbers_to_send = Numbers.get_all_numbers_only_by_area_id(area_id)
        if not numbers_to_send:
            return {'message': 'No numbers exist currently in this area', 'status': 'failed'}, 400
            
        sender_shortcode = Shortcodes.get_shortcode_only_by_id(shortcode_id)
        if not sender_shortcode:
            return {'message': 'Invalid shortcode', 'status': 'failed'}, 400

        # Calculate total cost
        total_credits = len(numbers_to_send) * BROADCAST_CREDIT_COST
        
        # Check and deduct credits
        credit_points = CreditPoints.get_by_user_id(get_jwt_identity())
        if not credit_points:
            return {'message': 'No credit points found', 'status': 'failed'}, 404
            
        success, usage = credit_points.deduct_credits(
            amount=total_credits,
            service_type='broadcast'
        )
        
        if not success:
            return {'message': 'Insufficient credits', 'status': 'failed'}, 400

        # Send messages
        failed_numbers = []
        success_count = 0
        
        for number in numbers_to_send:
            try:
                response = AfricasTalking().send(sender=sender_shortcode, message=message, recipients=number)
                if response["SMSMessageData"]["Recipients"][0]["statusCode"] == 101:
                    success_count += 1
                else:
                    failed_numbers.append(number)
            except Exception:
                failed_numbers.append(number)

        # Handle partial or complete failure
        if success_count == 0:
            # If all messages failed, refund all credits
            credit_points.refund_credits(total_credits, usage.id)
            return {'message': 'Broadcast failed for all numbers', 'status': 'failed'}, 500
            
        elif failed_numbers:
            # If some messages failed, refund credits for failed ones
            refund_amount = len(failed_numbers) * BROADCAST_CREDIT_COST
            credit_points.refund_credits(refund_amount, usage.id)
            
        # Create message record for successful sends
        if success_count > 0:
            messages = Messages.create(message, shortcode_id, user_id, area_id)
            
            return {
                'status': 'success',
                'message': 'Broadcast completed',
                'data': {
                    'message': MessagesSchema().dump(messages),
                    'total_recipients': len(numbers_to_send),
                    'successful_sends': success_count,
                    'failed_sends': len(failed_numbers),
                    'credits_used': total_credits - (len(failed_numbers) * BROADCAST_CREDIT_COST),
                    'credits_refunded': len(failed_numbers) * BROADCAST_CREDIT_COST if failed_numbers else 0,
                    'usage': CreditUsageSchema().dump(usage)
                }
            }, 200

    except Exception as e:
        # Refund credits if we caught an exception
        if 'usage' in locals() and 'credit_points' in locals():
            credit_points.refund_credits(total_credits, usage.id)
        return {'message': str(e), 'status': 'failed'}, 500

@bp.post('/messages/reply')
def respond_to_message():
    response = request.form
    chat_history = []
    sender_number = response.get('from')
    shortcode = response.get('to')
    message = response.get('text')
    
    try:
        # Get the user associated with the shortcode
        shortcode_obj = Shortcodes.get_by_shortcode(shortcode)
        if not shortcode_obj:
            return {'message': 'Invalid shortcode', 'status': 'failed'}, 400
            
        # Check and deduct credits
        credit_points = CreditPoints.get_by_user_id(shortcode_obj.user_id)
        if not credit_points:
            return {'message': 'No credit points found', 'status': 'failed'}, 404
            
        success, usage = credit_points.deduct_credits(
            amount=RESPONSE_CREDIT_COST,
            service_type='shortcode_response'
        )
        
        if not success:
            return {'message': 'Insufficient credits', 'status': 'failed'}, 400
            
        appended_message = f'{message}'
        number_exists = Numbers.check_if_number_exists(sender_number)
        user_language = Numbers.get_language_by_number(sender_number)

        try:
            if number_exists:
                answer = qa_chain(appended_message, chat_history, shortcode, user_language)
                send_result = AfricasTalking().send(sender=shortcode, message=answer, recipients=[sender_number])
                
                if send_result["SMSMessageData"]["Recipients"][0]["statusCode"] == 101:
                    return response, 200
                else:
                    raise Exception("Failed to send message")
            else:
                send_result = AfricasTalking().send(
                    sender=shortcode,
                    message="Your number is not registered in our system, please dial *347*875# to register.",
                    recipients=[sender_number]
                )
                if send_result["SMSMessageData"]["Recipients"][0]["statusCode"] == 101:
                    return response, 200
                else:
                    raise Exception("Failed to send message")
                    
        except Exception as e:
            # Refund credits if message sending failed
            credit_points.refund_credits(RESPONSE_CREDIT_COST, usage.id)
            raise e

    except Exception as e:
        # Refund credits if we caught an exception and have a transaction
        if 'usage' in locals() and 'credit_points' in locals():
            credit_points.refund_credits(RESPONSE_CREDIT_COST, usage.id)
        return {'message': str(e), 'status': 'failed'}, 500

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
            send_twilio_message(to=sender_number, message="Your number is not registered in our system, please register first to get responses.", from_=recipient_number)    
        
        
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
            send_twilio_message(to=sender_number, message="Your number is not registered in our system, please register first to get responses.", from_=recipient_number)    
        
        
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
    # If the result is already a list of dicts (from join), return as is
    if messagess and isinstance(messagess[0], dict):
        return {'data': messagess, 'message': 'Messages fetched successfully', 'status': 'success'}, 200
    return {'data': MessagesSchema(many=True).dump(messagess), 'message': 'Messages fetched successfully', 'status': 'success'}, 200