"""added posts model

Revision ID: 768ae1a6d45c
Revises: 42961e34d82b
Create Date: 2024-03-27 11:25:50.307054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '768ae1a6d45c'
down_revision = '42961e34d82b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('shopname', sa.String(length=100), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('shopowner', sa.String(length=100), nullable=True),
    sa.Column('address', sa.String(length=150), nullable=True),
    sa.Column('contact', sa.String(length=10), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=True),
    sa.Column('slug', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    # ### end Alembic commands ###