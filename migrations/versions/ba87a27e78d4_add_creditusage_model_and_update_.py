"""Add CreditUsage model and update CreditTransaction (idempotent)

Revision ID: ba87a27e78d4
Revises: 9eecb7911adc
Create Date: 2025-05-30 21:09:15.003845
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import inspect as _inspect

# revision identifiers, used by Alembic.
revision = "ba87a27e78d4"
down_revision = "9eecb7911adc"
branch_labels = None
depends_on = None

def _insp():
    return _inspect(op.get_bind())

def _has_table(name: str) -> bool:
    return name in _insp().get_table_names()

def _has_column(table: str, column: str) -> bool:
    return column in [c["name"] for c in _insp().get_columns(table)]

def _col_nullable(table: str, column: str) -> bool:
    for c in _insp().get_columns(table):
        if c["name"] == column:
            return bool(c.get("nullable", True))
    return True

def upgrade():
    # --- CREDIT USAGE TABLE ---
    if not _has_table("credit_usage"):
        op.create_table(
            "credit_usage",
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"), nullable=False),
            sa.Column("amount", sa.Float, nullable=False),
            sa.Column("service_type", sa.String(length=50), nullable=False),
            sa.Column("is_refunded", sa.Boolean, nullable=False),
            sa.Column("created_at", postgresql.TIMESTAMP(), nullable=False),
            sa.Column("refunded_at", postgresql.TIMESTAMP(), nullable=True),
        )
    else:
        # If table exists, only add/fix what's missing
        with op.batch_alter_table("credit_usage", schema=None) as batch_op:
            if not _has_column("credit_usage", "user_id"):
                batch_op.add_column(sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"), nullable=False))
            if not _has_column("credit_usage", "amount"):
                batch_op.add_column(sa.Column("amount", sa.Float, nullable=False))
            if not _has_column("credit_usage", "service_type"):
                batch_op.add_column(sa.Column("service_type", sa.String(length=50), nullable=False))
            if not _has_column("credit_usage", "is_refunded"):
                batch_op.add_column(sa.Column("is_refunded", sa.Boolean, nullable=False))
            if not _has_column("credit_usage", "created_at"):
                batch_op.add_column(sa.Column("created_at", postgresql.TIMESTAMP(), nullable=False))
            if not _has_column("credit_usage", "refunded_at"):
                batch_op.add_column(sa.Column("refunded_at", postgresql.TIMESTAMP(), nullable=True))

            # Tighten nullability only if currently nullable
            if _has_column("credit_usage", "is_refunded") and _col_nullable("credit_usage", "is_refunded"):
                batch_op.alter_column("is_refunded", existing_type=sa.BOOLEAN(), nullable=False)
            if _has_column("credit_usage", "created_at") and _col_nullable("credit_usage", "created_at"):
                batch_op.alter_column("created_at", existing_type=postgresql.TIMESTAMP(), nullable=False)

    # --- CREDIT TRANSACTION: drop legacy column only if present ---
    with op.batch_alter_table("credit_transaction", schema=None) as batch_op:
        if _has_column("credit_transaction", "transaction_type"):
            batch_op.drop_column("transaction_type")

def downgrade():
    # Keep reversible only for the transaction_type
    with op.batch_alter_table("credit_transaction", schema=None) as batch_op:
        if not _has_column("credit_transaction", "transaction_type"):
            batch_op.add_column(sa.Column("transaction_type", sa.VARCHAR(), nullable=False))
    # Avoid dropping credit_usage to prevent data loss
    pass
