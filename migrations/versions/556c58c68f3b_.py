"""empty message

Revision ID: 556c58c68f3b
Revises: 259e12606c79
Create Date: 2024-07-26 17:07:57.301829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '556c58c68f3b'
down_revision = '259e12606c79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('venue_genres',
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['genre_id'], ['Genre.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('venue_id', 'genre_id')
    )
    op.create_table('artist_genres',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['genre_id'], ['Genre.id'], ),
    sa.PrimaryKeyConstraint('artist_id', 'genre_id')
    )
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('city_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('state_id', sa.String(length=2), nullable=False))
        batch_op.create_foreign_key(None, 'City', ['city_id'], ['id'])
        batch_op.create_foreign_key(None, 'State', ['state_id'], ['id'])
        batch_op.drop_column('state')
        batch_op.drop_column('city')
        batch_op.drop_column('genres')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('state_id')
        batch_op.drop_column('city_id')

    op.drop_table('artist_genres')
    op.drop_table('venue_genres')
    # ### end Alembic commands ###