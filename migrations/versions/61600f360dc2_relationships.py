"""relationships

Revision ID: 61600f360dc2
Revises: 65bd36b54e90
Create Date: 2024-07-26 17:44:30.190722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61600f360dc2'
down_revision = '65bd36b54e90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('city_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('state_id', sa.String(length=2), nullable=False))
        batch_op.create_foreign_key(None, 'State', ['state_id'], ['id'])
        batch_op.create_foreign_key(None, 'City', ['city_id'], ['id'])
        batch_op.drop_column('state')
        batch_op.drop_column('city')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('state_id')
        batch_op.drop_column('city_id')

    # ### end Alembic commands ###