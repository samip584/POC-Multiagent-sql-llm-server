"""Initial migration - create all tables

Revision ID: 001
Revises: 
Create Date: 2025-11-19 19:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone', sa.BigInteger(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('idp_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create places table
    op.create_table('places',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create media table
    op.create_table('media',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('external_resource_url', sa.String(), nullable=True),
        sa.Column('meta', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create timelines table
    op.create_table('timelines',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('start_timestamp', sa.Integer(), nullable=True),
        sa.Column('end_timestamp', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('places_id', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create follow table
    op.create_table('follow',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_user_id', sa.Integer(), nullable=True),
        sa.Column('destination_user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['destination_user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['source_user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create posts table
    op.create_table('posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('media_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['media_id'], ['media.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('posts')
    op.drop_table('follow')
    op.drop_table('timelines')
    op.drop_table('media')
    op.drop_table('places')
    op.drop_table('users')
