"""Increase password_hash column size

Revision ID: 470c67b5fe12
Revises: 65f5826f3e29
Create Date: 2025-04-20 19:00:45.965316

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '470c67b5fe12'
down_revision = '65f5826f3e29'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=256),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=128),
               existing_nullable=True)

    # ### end Alembic commands ###
