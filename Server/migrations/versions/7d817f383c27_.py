"""empty message

Revision ID: 7d817f383c27
Revises: e766f638a302
Create Date: 2023-05-03 11:14:41.081573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d817f383c27'
down_revision = 'e766f638a302'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket_comments', schema=None) as batch_op:
        batch_op.alter_column('ticket_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket_comments', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('ticket_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
