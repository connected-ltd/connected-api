from flask import Blueprint, g, request
from app.route_guard import auth_required
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
import asyncio
import os

from app.messages.model import *
from app.messages.schema import *
from app.numbers.schema import *
from app.numbers.model import *
from app.shortcodes.model import *
from app.files.model import *
from app.credit.model import CreditPoints, CreditUsage, CreditTransaction
from app.credit.schema import CreditUsageSchema
from app.whatsapp_number.model import *
from helpers.africastalking import AfricasTalking
from helpers.twilio import send_twilio_message
from helpers.gemini_langchain import gemini_qa_chain
from helpers.hollatags import send_sms

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
        user_id = g.user.id
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
                if response["SMSMessageData"]["Recipients"][0]["status"] == 'Success':
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
        user_obj = Shortcodes.get_user_by_shortcode(shortcode)
        if not user_obj:
            return {'message': 'Invalid shortcode', 'status': 'failed'}, 400
        
        # Get the shortcode row
        shortcode_row = Shortcodes.get_by_user_id(user_obj.id)
        if not shortcode_row:
            return {'message': 'Shortcode row not found', 'status': 'failed'}, 404

        # Check and deduct credits
        credit_points = CreditPoints.get_by_user_id(user_obj.id)
        if not credit_points:
            return {'message': 'No credit points found', 'status': 'failed'}, 404
            
        success, usage = credit_points.deduct_credits(
            amount=RESPONSE_CREDIT_COST,
            service_type='shortcode_response'
        )
        
        if not success:
            return {'message': 'Insufficient credits', 'status': 'failed'}, 400

        try:
            from app.files.model import Files
            file_exists = Files.query.filter_by(shortcode_id=shortcode_row.id, is_deleted=False).first()

            if not file_exists:
                send_result = AfricasTalking().send(
                    sender=shortcode,
                    message="Sorry, no information has been uploaded for this shortcode yet. Please check back later.",
                    recipients=[sender_number]
                )
                if send_result["SMSMessageData"]["Recipients"][0]["status"] == 'Success':
                    return response, 200
                else:
                    raise Exception("Failed to send message")
            
            number_exists = Numbers.check_if_number_exists(sender_number)
            user_language = Numbers.get_language_by_number(sender_number)

            if number_exists:
                answer = gemini_qa_chain(message, chat_history, shortcode, user_language)
                send_result = AfricasTalking().send(
                    sender=shortcode, 
                    message=answer, 
                    recipients=[sender_number]
                )
                if send_result["SMSMessageData"]["Recipients"][0]["status"] == 'Success':
                    return response, 200
                else:
                    raise Exception("Failed to send message")
            else:
                send_result = AfricasTalking().send(
                    sender=shortcode,
                    message="Your number is not registered in our system, please dial *347*875# to register.",
                    recipients=[sender_number]
                )
                if send_result["SMSMessageData"]["Recipients"][0]["status"] == 'Success':
                    return response, 200
                else:
                    raise Exception("Failed to send message")
                    
        except Exception as e:
            # Only refund if message failed to send
            credit_points.refund_credits(RESPONSE_CREDIT_COST, usage.id)
            raise e

    except Exception as e:
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
        
        formatted_sender_number = sender_number.split(':')[1].strip()
        formatted_recipient_number = recipient_number.split('+')[1].strip()

        # Get the user_id from the whatsapp number
        user_id = Whatsapp_Number.get_user_id_by_number(f'+{formatted_recipient_number}')
        if not user_id:
            return {'message': 'Invalid whatsapp number', 'status': 'failed'}, 400

        # Check and deduct credits
        credit_points = CreditPoints.get_by_user_id(user_id)
        if not credit_points:
            return {'message': 'No credit points found', 'status': 'failed'}, 404

        success, usage = credit_points.deduct_credits(
            amount=RESPONSE_CREDIT_COST,
            service_type='whatsapp_response'
        )

        if not success:
            return {'message': 'Insufficient credits', 'status': 'failed'}, 400

        try:
            number_exists = Numbers.check_if_number_exists(formatted_sender_number)
            user_language = Numbers.get_language_by_number(formatted_sender_number)

            if number_exists:
                answer = gemini_qa_chain(message, chat_history, formatted_recipient_number, user_language, max_response_length=1500)
                send_twilio_message(to=sender_number, message=answer, from_=recipient_number)
            else:
                send_twilio_message(
                    to=sender_number, 
                    message="Your number is not registered in our system, please register first to get responses.", 
                    from_=recipient_number
                )

            return response

        except Exception as e:
            credit_points.refund_credits(RESPONSE_CREDIT_COST, usage.id)
            raise e

    except Exception as e:
        if 'usage' in locals() and 'credit_points' in locals():
            credit_points.refund_credits(RESPONSE_CREDIT_COST, usage.id)
        return {'message': str(e), 'status': 'failed'}, 500


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
        
        formatted_recipient_number = recipient_number.split('+')[1].strip()

        # Get the user_id from the whatsapp number
        user_id = Whatsapp_Number.get_user_id_by_number(f'+{formatted_recipient_number}')
        if not user_id:
            return {'message': 'Invalid number', 'status': 'failed'}, 400

        # Check and deduct credits
        credit_points = CreditPoints.get_by_user_id(user_id)
        if not credit_points:
            return {'message': 'No credit points found', 'status': 'failed'}, 404

        success, usage = credit_points.deduct_credits(
            amount=RESPONSE_CREDIT_COST,
            service_type='sms_response'
        )

        if not success:
            return {'message': 'Insufficient credits', 'status': 'failed'}, 400

        try:
            number_exists = Numbers.check_if_number_exists(sender_number)
            user_language = Numbers.get_language_by_number(sender_number)

            if number_exists:
                answer = gemini_qa_chain(message, chat_history, formatted_recipient_number, user_language)
                send_twilio_message(to=sender_number, message=answer, from_=recipient_number)
            else:
                send_twilio_message(
                    to=sender_number, 
                    message="Your number is not registered in our system, please register first to get responses.", 
                    from_=recipient_number
                )

            return response

        except Exception as e:
            credit_points.refund_credits(RESPONSE_CREDIT_COST, usage.id)
            raise e

    except Exception as e:
        if 'usage' in locals() and 'credit_points' in locals():
            credit_points.refund_credits(RESPONSE_CREDIT_COST, usage.id)
        return {'message': str(e), 'status': 'failed'}, 500
    

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