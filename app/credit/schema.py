from app import ma
from app.credit.model import CreditPoints, CreditTransaction, CreditUsage

class CreditPointsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CreditPoints
        exclude = ('is_deleted',)

class CreditTransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CreditTransaction
        exclude = ('is_deleted',)

class CreditUsageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CreditUsage 