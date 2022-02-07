"""Add MenuCategory.description field

Revision ID: 9dd8856b05c4
Revises: d51652bf8f5b
Create Date: 2022-02-06 22:13:33.970043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9dd8856b05c4'
down_revision = 'd51652bf8f5b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('menu_categories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('menu_categories', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
