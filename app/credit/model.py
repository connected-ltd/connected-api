from app import db
from datetime import datetime

class CreditPoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id, is_deleted=False).first()

    @classmethod
    def create(cls, user_id):
        credit = cls(user_id=user_id)
        db.session.add(credit)
        db.session.commit()
        return credit

    def add_credits(self, amount):
        self.balance += amount
        self.updated_at = db.func.now()
        db.session.commit()
        return self

    def deduct_credits(self, amount, service_type=None):
        """Deduct credits and log usage"""
        if self.balance < amount:
            # This case should not be happening based on the debug logs (90.0 < 0.6 is false)
            print(f"DEBUG: deduct_credits returning False due to self.balance ({self.balance}) < amount ({amount})")
            return False, None
        
        try:
            # Start transaction
            self.balance -= amount
            self.updated_at = db.func.now()
            
            # Log the usage
            print(f"DEBUG: Attempting to create CreditUsage: user_id={self.user_id}, amount={amount}, service_type={service_type}")
            usage = CreditUsage.create(
                user_id=self.user_id,
                amount=amount,
                service_type=service_type
            )
            print(f"DEBUG: CreditUsage created successfully: id={usage.id if usage else 'None'}")
            
            db.session.commit()
            print("DEBUG: deduct_credits main db.session.commit() successful")
            return True, usage
            
        except Exception as e:
            print(f"DEBUG: Exception in deduct_credits: {str(e)}") # Add this line to print the exception
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")   # Add this for full traceback
            db.session.rollback()
            print("DEBUG: deduct_credits db.session.rollback() executed due to exception")
            return False, None

    def refund_credits(self, amount, usage_id):
        """Refund credits and mark usage as refunded"""
        try:
            self.balance += amount
            self.updated_at = db.func.now()
            
            usage = CreditUsage.query.get(usage_id)
            if usage:
                usage.is_refunded = True
                usage.refunded_at = db.func.now()
                
            db.session.commit()
            return True
            
        except Exception:
            db.session.rollback()
            return False

class CreditTransaction(db.Model):
    """Model for payment transactions (Paystack)"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    reference = db.Column(db.String(100), unique=True)  # Paystack reference
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, success, failed
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    @classmethod
    def create(cls, user_id, amount, reference):
        transaction = cls(
            user_id=user_id,
            amount=amount,
            reference=reference
        )
        db.session.add(transaction)
        db.session.commit()
        return transaction

    @classmethod
    def get_by_reference(cls, reference):
        return cls.query.filter_by(reference=reference, is_deleted=False).first()

    def update_status(self, status):
        self.status = status
        db.session.commit()
        return self

class CreditUsage(db.Model):
    """Model for tracking credit usage within the application"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    service_type = db.Column(db.String(50), nullable=False)  # 'broadcast', 'shortcode_response'
    is_refunded = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    refunded_at = db.Column(db.DateTime, nullable=True)

    @classmethod
    def create(cls, user_id, amount, service_type):
        usage = cls(
            user_id=user_id,
            amount=amount,
            service_type=service_type
        )
        db.session.add(usage)
        db.session.commit()
        return usage

    @classmethod
    def get_user_usage(cls, user_id, service_type=None):
        query = cls.query.filter_by(user_id=user_id)
        if service_type:
            query = query.filter_by(service_type=service_type)
        return query.order_by(cls.created_at.desc()).all() 