"""add last few collums  to post table

Revision ID: 0cc1b13155bf
Revises: f61340bd5162
Create Date: 2023-03-13 01:32:51.284467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cc1b13155bf'
down_revision = 'f61340bd5162'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    op.add_column('posts', sa.Column('votes', sa.Integer(), nullable=False, server_default='1') )          
    pass


def downgrade() -> None:
    op.drop_column('posts', 'votes')
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    pass
