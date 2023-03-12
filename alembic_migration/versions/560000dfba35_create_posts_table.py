"""create posts table

Revision ID: 560000dfba35
Revises: 
Create Date: 2023-03-13 00:52:14.661601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '560000dfba35'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
