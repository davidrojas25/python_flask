"""added group column

Revision ID: cb8fef406c0c
Revises: 
Create Date: 2020-05-17 07:00:27.412136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb8fef406c0c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('runners', sa.Column('group', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('runners', 'group')
    # ### end Alembic commands ###
