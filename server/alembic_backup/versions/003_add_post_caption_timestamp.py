"""Add post caption and timestamp

Revision ID: 003
Revises: 002
Create Date: 2025-11-19 20:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('caption', sa.Text(), nullable=True))
    op.add_column('posts', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('posts', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'updated_at')
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'caption')
