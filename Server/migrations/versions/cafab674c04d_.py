"""empty message

Revision ID: cafab674c04d
Revises: 7d817f383c27
Create Date: 2023-05-03 13:30:37.931491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cafab674c04d'
down_revision = '7d817f383c27'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=True))
        batch_op.drop_column('role')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_column('is_admin')

    # ### end Alembic commands ###