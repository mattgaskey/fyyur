"""empty message

Revision ID: 65bd36b54e90
Revises: 556c58c68f3b
Create Date: 2024-07-26 17:35:42.200288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65bd36b54e90'
down_revision = '556c58c68f3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('website_link', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('seeking_talent', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('seeking_description', sa.String(length=500), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.drop_column('seeking_description')
        batch_op.drop_column('seeking_talent')
        batch_op.drop_column('website_link')

    # ### end Alembic commands ###