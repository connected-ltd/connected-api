import os

PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')
if not PAYSTACK_SECRET_KEY:
    raise ValueError("PAYSTACK_SECRET_KEY environment variable is not set") 