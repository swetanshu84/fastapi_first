"""add foreign-key to post table

Revision ID: f61340bd5162
Revises: 97455231d259
Create Date: 2023-03-13 01:25:27.387682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f61340bd5162'
down_revision = '97455231d259'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fkey', source_table='posts', referent_table= 'users', local_cols= ['owner_id'], remote_cols= ['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
