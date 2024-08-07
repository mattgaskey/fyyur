"""artist availability

Revision ID: 518f5329abe0
Revises: de46350148c1
Create Date: 2024-07-31 01:47:07.713037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '518f5329abe0'
down_revision = 'de46350148c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('available_start_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('available_end_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('available_start_time', sa.Time(), nullable=True))
        batch_op.add_column(sa.Column('available_end_time', sa.Time(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.drop_column('available_end_time')
        batch_op.drop_column('available_start_time')
        batch_op.drop_column('available_end_date')
        batch_op.drop_column('available_start_date')

    # ### end Alembic commands ###
