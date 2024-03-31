"""small edit in hometwon

Revision ID: 0e053225c3c2
Revises: 
Create Date: 2024-03-26 22:45:02.725735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e053225c3c2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hometown', sa.String(length=120), nullable=False , server_default=''))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('hometown')

    # ### end Alembic commands ###
