"""Add reference and status columns to credit_transaction (idempotent with checks)"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import inspect as _inspect

revision = "9eecb7911adc"
down_revision = "credit_points_tables"
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

def _has_unique_by_name(table: str, name: str) -> bool:
    return any(u["name"] == name for u in _insp().get_unique_constraints(table))

def _has_unique_on_cols(table: str, cols: list[str]) -> bool:
    want = set(cols)
    for u in _insp().get_unique_constraints(table):
        if set(u.get("column_names") or []) == want:
            return True
    return False

def _has_check(table: str, name: str) -> bool:
    return any(c["name"] == name for c in _insp().get_check_constraints(table))

def upgrade():
    # credit_points: tighten NOT NULL if currently nullable
    with op.batch_alter_table("credit_points", schema=None) as batch_op:
        if _col_nullable("credit_points", "created_at"):
            batch_op.alter_column("created_at", existing_type=postgresql.TIMESTAMP(), nullable=False)
        if _col_nullable("credit_points", "updated_at"):
            batch_op.alter_column("updated_at", existing_type=postgresql.TIMESTAMP(), nullable=False)
        if _col_nullable("credit_points", "is_deleted"):
            batch_op.alter_column("is_deleted", existing_type=sa.BOOLEAN(), nullable=False)

    # credit_transaction: add/adjust idempotently
    with op.batch_alter_table("credit_transaction", schema=None) as batch_op:
        if not _has_column("credit_transaction", "reference"):
            batch_op.add_column(sa.Column("reference", sa.String(length=100), nullable=True))
        if not _has_column("credit_transaction", "status"):
            batch_op.add_column(sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"))
        if _col_nullable("credit_transaction", "created_at"):
            batch_op.alter_column("created_at", existing_type=postgresql.TIMESTAMP(), nullable=False)
        if _col_nullable("credit_transaction", "is_deleted"):
            batch_op.alter_column("is_deleted", existing_type=sa.BOOLEAN(), nullable=False)
        # unique on reference (by name or by column set)
        if _has_column("credit_transaction", "reference") and not (
            _has_unique_by_name("credit_transaction", "credit_transaction_reference_key")
            or _has_unique_on_cols("credit_transaction", ["reference"])
        ):
            batch_op.create_unique_constraint("credit_transaction_reference_key", ["reference"])
        # drop legacy description if present
        if _has_column("credit_transaction", "description"):
            batch_op.drop_column("description")

    # sanitize status values and add CHECK
    op.execute("""
        UPDATE credit_transaction
        SET status = 'pending'
        WHERE status IS NULL OR status NOT IN ('pending','success','failed')
    """)
    with op.batch_alter_table("credit_transaction", schema=None) as batch_op:
        if not _has_check("credit_transaction", "credit_transaction_status_check"):
            batch_op.create_check_constraint(
                "credit_transaction_status_check",
                "status IN ('pending','success','failed')"
            )
        # keep default or drop it; uncomment next line to drop default:
        # batch_op.alter_column("status", server_default=None)

def downgrade():
    with op.batch_alter_table("credit_transaction", schema=None) as batch_op:
        try:
            batch_op.drop_constraint("credit_transaction_status_check", type_="check")
        except Exception:
            pass
        try:
            batch_op.drop_constraint("credit_transaction_reference_key", type_="unique")
        except Exception:
            pass
        if _has_column("credit_transaction", "status"):
            batch_op.drop_column("status")
        if _has_column("credit_transaction", "reference"):
            batch_op.drop_column("reference")
