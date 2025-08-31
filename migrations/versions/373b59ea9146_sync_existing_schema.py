"""sync existing schema

Revision ID: 373b59ea9146
Revises: b87bb612551e
Create Date: 2025-08-31 11:42:55.449807
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect as _inspect

# revision identifiers, used by Alembic.
revision = '373b59ea9146'
down_revision = 'b87bb612551e'
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

def upgrade():
    # --- COMPANY NAME backfill (unique) ---
    if _has_column('user', 'company_name') and _has_column('user', 'username'):
        op.execute("""
            UPDATE "user" u
               SET company_name = u.username
             WHERE (u.company_name IS NULL OR u.company_name = '')
               AND u.username IS NOT NULL AND u.username <> ''
               AND NOT EXISTS (
                     SELECT 1 FROM "user" u2
                      WHERE u2.username = u.username
                        AND u2.id <> u.id
               )
        """)

        # Now safe to enforce NOT NULL
        if _col_nullable('user', 'company_name'):
            with op.batch_alter_table('user', schema=None) as batch_op:
                batch_op.alter_column('company_name', existing_type=sa.VARCHAR(), nullable=False)
        # ensure no server default remains
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.alter_column('company_name', server_default=None)

    # --- ROLE backfill and NOT NULL ---
    if _has_column('user', 'role'):
        # Backfill NULL/empty roles to 'organization'
        op.execute("""
            UPDATE "user"
               SET role = 'organization'
             WHERE role IS NULL OR role = ''
        """)
        # Enforce NOT NULL
        if _col_nullable('user', 'role'):
            with op.batch_alter_table('user', schema=None) as batch_op:
                batch_op.alter_column('role', existing_type=sa.VARCHAR(), nullable=False)
                batch_op.alter_column('role', server_default=None)

def downgrade():
    # Relax constraints if downgrading
    if _has_column('user', 'role'):
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.alter_column('role', existing_type=sa.VARCHAR(), nullable=True)
    if _has_column('user', 'company_name'):
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.alter_column('company_name', existing_type=sa.VARCHAR(), nullable=True)
            batch_op.alter_column('company_name', server_default=None)