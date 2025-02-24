"""Add Users table for auth

Revision ID: b0555527ec0e
Revises: 091ec8dd2983
Create Date: 2021-12-23 18:19:08.081772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0555527ec0e'
down_revision = '091ec8dd2983'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_created', sa.DateTime, nullable=False),
    sa.Column('date_modified', sa.DateTime, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=True)

    from sqlalchemy.orm import Session
    from src.models import User
    session = Session(bind=op.get_bind())
    session.add(
        User(name='vicki', hashed_password='$2b$12$5BkzVQgGaJ6qOIyQSrW2Wu8BBb6X6gp2aQDkH27ClZCdgS2eOeMxa')
    )
    session.commit()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
