"""add credit points tables

Revision ID: credit_points_tables
Revises: b87bb612551e
Create Date: 2024-03-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect as _inspect

def _has_table(name: str) -> bool:
    bind = op.get_bind()
    insp = _inspect(bind)
    return name in insp.get_table_names()


# revision identifiers, used by Alembic.
revision = 'credit_points_tables'
down_revision = 'b87bb612551e'
branch_labels = None
depends_on = None

def upgrade():
    # Create credit_points table
    if not _has_table('credit_points'):
        op.create_table('credit_points',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('balance', sa.Float(), nullable=False, default=0.0),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.Column('is_deleted', sa.Boolean(), nullable=True),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

    # Create credit_transaction table
    if not _has_table('credit_transaction'):
        op.create_table('credit_transaction',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('amount', sa.Float(), nullable=False),
            sa.Column('transaction_type', sa.String(), nullable=False),
            sa.Column('description', sa.String(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('is_deleted', sa.Boolean(), nullable=True),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

def downgrade():
    op.drop_table('credit_transaction')
    op.drop_table('credit_points') 