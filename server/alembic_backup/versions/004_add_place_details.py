"""Add place category and description

Revision ID: 004
Revises: 003
Create Date: 2025-11-19 21:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('places', sa.Column('category', sa.String(), nullable=True))
    op.add_column('places', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('places', sa.Column('address', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('places', 'address')
    op.drop_column('places', 'description')
    op.drop_column('places', 'category')
