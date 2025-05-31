from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
from app.route_guard import auth_required
from app.credit.model import CreditPoints, CreditTransaction
from app.credit.schema import CreditPointsSchema, CreditTransactionSchema
from app.user.model import User

bp = Blueprint('credit', __name__)

CREDIT_RATE = 10  # 1 credit = 10 naira

@bp.post('/credits/initialize-payment')
@jwt_required()
def initialize_payment():
    """Initialize a Paystack payment for credits"""
    try:
        amount_in_naira = float(request.json.get('amount', 0))
        if amount_in_naira <= 0:
            return {'message': 'Invalid amount', 'status': 'failed'}, 400

        # Amount must be a multiple of CREDIT_RATE to get whole credits
        if amount_in_naira % CREDIT_RATE != 0:
            return {
                'message': f'Amount must be a multiple of {CREDIT_RATE} naira to convert to whole credits', 
                'status': 'failed'
            }, 400

        credits = amount_in_naira / CREDIT_RATE
        amount_in_kobo = int(amount_in_naira * 100)  # Paystack expects amount in kobo

        user = User.get_by_id(get_jwt_identity())
        if not user:
            return {'message': 'User not found', 'status': 'failed'}, 404

        # Initialize transaction with Paystack
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}",
            "Content-Type": "application/json"
        }
        data = {
            "email": user.username,
            "amount": amount_in_kobo,
            "metadata": {
                "credits": credits,
                "user_id": user.id
            }
        }

        response = requests.post(url, headers=headers, json=data)
        if not response.ok:
            return {'message': 'Payment initialization failed', 'status': 'failed'}, 400

        result = response.json()
        if not result.get('status'):
            return {'message': 'Payment initialization failed', 'status': 'failed'}, 400

        # Create a pending transaction
        transaction = CreditTransaction.create(
            user_id=user.id,
            amount=credits,
            transaction_type='add',
            reference=result['data']['reference']
        )

        return {
            'message': 'Payment initialized successfully',
            'status': 'success',
            'data': {
                'authorization_url': result['data']['authorization_url'],
                'reference': result['data']['reference'],
                'transaction': CreditTransactionSchema().dump(transaction)
            }
        }, 200

    except Exception as e:
        return {'message': str(e), 'status': 'failed'}, 500

@bp.post('/credits/verify-payment')
@jwt_required()
def verify_payment():
    """Verify a Paystack payment and add credits"""
    try:
        reference = request.json.get('reference')
        if not reference:
            return {'message': 'Reference is required', 'status': 'failed'}, 400

        transaction = CreditTransaction.get_by_reference(reference)
        if not transaction:
            return {'message': 'Transaction not found', 'status': 'failed'}, 404

        if transaction.status == 'success':
            return {'message': 'Transaction already processed', 'status': 'success'}, 200

        # Verify with Paystack
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {current_app.config['PAYSTACK_SECRET_KEY']}"
        }

        response = requests.get(url, headers=headers)
        if not response.ok:
            transaction.update_status('failed')
            return {'message': 'Payment verification failed', 'status': 'failed'}, 400

        result = response.json()
        if not result.get('status') or result['data']['status'] != 'success':
            transaction.update_status('failed')
            return {'message': 'Payment was not successful', 'status': 'failed'}, 400

        # Add credits to user's balance
        credit_points = CreditPoints.get_by_user_id(transaction.user_id)
        if not credit_points:
            credit_points = CreditPoints.create(transaction.user_id)

        credit_points.add_credits(transaction.amount)
        transaction.update_status('success')

        return {
            'message': 'Payment verified and credits added successfully',
            'status': 'success',
            'data': {
                'credit_points': CreditPointsSchema().dump(credit_points),
                'transaction': CreditTransactionSchema().dump(transaction)
            }
        }, 200

    except Exception as e:
        return {'message': str(e), 'status': 'failed'}, 500

@bp.get('/credits/balance')
@jwt_required()
def get_balance():
    """Get user's credit balance"""
    try:
        credit_points = CreditPoints.get_by_user_id(get_jwt_identity())
        if not credit_points:
            credit_points = CreditPoints.create(get_jwt_identity())
        
        return {
            'message': 'Balance retrieved successfully',
            'status': 'success',
            'data': CreditPointsSchema().dump(credit_points)
        }, 200

    except Exception as e:
        return {'message': str(e), 'status': 'failed'}, 500

@bp.get('/credits/transactions')
@jwt_required()
def get_transactions():
    """Get user's credit transactions history"""
    try:
        user_id = get_jwt_identity()
        transactions = CreditTransaction.get_by_user_id(user_id)
        
        # Add Naira amounts to transaction data
        transaction_data = CreditTransactionSchema(many=True).dump(transactions)
        for transaction in transaction_data:
            transaction['amount_in_naira'] = transaction['amount'] * CREDIT_RATE
        
        return {
            'status': 'success',
            'data': transaction_data
        }, 200

    except Exception as e:
        return {'message': str(e), 'status': 'failed'}, 500

@bp.post('/credits/deduct')
@jwt_required()
def deduct_credits():
    """Deduct credits from user's balance"""
    try:
        amount = float(request.json.get('amount', 0))
        if amount <= 0:
            return {'message': 'Invalid amount', 'status': 'failed'}, 400

        user_id = get_jwt_identity()
        credit_points = CreditPoints.get_by_user_id(user_id)
        if not credit_points:
            return {'message': 'No credits found', 'status': 'failed'}, 404

        if credit_points.deduct_credits(amount):
            return {
                'status': 'success',
                'message': 'Credits deducted successfully',
                'data': {
                    'amount_deducted': amount,
                    'amount_in_naira': amount * CREDIT_RATE,
                    'new_balance': credit_points.balance,
                    'new_balance_in_naira': credit_points.balance * CREDIT_RATE
                }
            }, 200
        return {'message': 'Insufficient credits', 'status': 'failed'}, 400

    except Exception as e:
        return {'message': str(e), 'status': 'failed'}, 500 