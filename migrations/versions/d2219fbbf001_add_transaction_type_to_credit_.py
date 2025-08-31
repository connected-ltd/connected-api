"""add_transaction_type_to_credit_transaction (idempotent)"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect as _inspect

revision = "d2219fbbf001"
down_revision = "ba87a27e78d4"
branch_labels = None
depends_on = None

def _insp():
    return _inspect(op.get_bind())

def _has_column(table: str, column: str) -> bool:
    return column in [c["name"] for c in _insp().get_columns(table)]

def _col_nullable(table: str, column: str) -> bool:
    for c in _insp().get_columns(table):
        if c["name"] == column:
            return bool(c.get("nullable", True))
    return True

def _has_check(table: str, name: str) -> bool:
    return any(c["name"] == name for c in _insp().get_check_constraints(table))

def upgrade():
    # Add as nullable with temp default, backfill, then enforce NOT NULL + CHECK.
    with op.batch_alter_table("credit_transaction", schema=None) as batch_op:
        if not _has_column("credit_transaction", "transaction_type"):
            batch_op.add_column(sa.Column("transaction_type", sa.String(length=20), nullable=True, server_default="add"))
        else:
            if _col_nullable("credit_transaction", "transaction_type"):
                batch_op.alter_column("transaction_type", server_default="add")

    # Backfill by rule: amount < 0 -> 'deduct', else 'add' (0 -> 'add')
    op.execute("""
        UPDATE credit_transaction
        SET transaction_type = CASE WHEN amount < 0 THEN 'deduct' ELSE 'add' END
        WHERE transaction_type IS NULL OR transaction_type NOT IN ('add','deduct')
    """)

    with op.batch_alter_table("credit_transaction", schema=None) as batch_op:
        if _col_nullable("credit_transaction", "transaction_type"):
            batch_op.alter_column("transaction_type", existing_type=sa.String(length=20), nullable=False)
        batch_op.alter_column("transaction_type", server_default=None)
        if not _has_check("credit_transaction", "credit_transaction_transaction_type_check"):
            batch_op.create_check_constraint(
                "credit_transaction_transaction_type_check",
                "transaction_type IN ('add','deduct')"
            )

def downgrade():
    with op.batch_alter_table("credit_transaction", schema=None) as batch_op:
        try:
            batch_op.drop_constraint("credit_transaction_transaction_type_check", type_="check")
        except Exception:
            pass
        if _has_column("credit_transaction", "transaction_type"):
            batch_op.drop_column("transaction_type")
