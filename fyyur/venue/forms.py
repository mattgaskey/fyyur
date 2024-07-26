from wtforms import StringField, SelectField, SelectMultipleField, BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL
import sqlalchemy as sa
from fyyur import db
from fyyur.models import State, Genre

class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        'website_link', validators=[URL()]
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )

    def __init__(self, *args, **kwargs):
        super(VenueForm, self).__init__(*args, **kwargs)
        states = db.session.scalars(sa.select(State)).all()
        self.state.choices = [(state.id, state.id) for state in states]
        genres = db.session.scalars(sa.select(Genre)).all()
        self.genres.choices = [(genre.id, genre.name) for genre in genres]