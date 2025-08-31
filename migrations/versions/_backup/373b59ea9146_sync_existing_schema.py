"""sync existing schema

Revision ID: 373b59ea9146
Revises: b87bb612551e
Create Date: 2025-08-31 11:42:55.449807
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '373b59ea9146'
down_revision = 'b87bb612551e'
branch_labels = None
depends_on = None


def upgrade():
    # Make only the intended changes; do NOT drop any tables.
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column(
            'company_name',
            existing_type=sa.VARCHAR(),
            nullable=False,
            existing_nullable=True,
        )
        batch_op.alter_column(
            'role',
            existing_type=sa.VARCHAR(),
            nullable=False,
            existing_nullable=True,
        )


def downgrade():
    # Revert only the above changes.
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column(
            'role',
            existing_type=sa.VARCHAR(),
            nullable=True,
            existing_nullable=False,
        )
        batch_op.alter_column(
            'company_name',
            existing_type=sa.VARCHAR(),
            nullable=True,
            existing_nullable=False,
        )
