from wtforms import StringField, SelectField, SelectMultipleField, BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL
import sqlalchemy as sa
from fyyur import db
from fyyur.models import State, Genre

class ArtistForm(FlaskForm):
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
    phone = StringField(
        # TODO implement validation logic for phone 
        'phone'
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[]
     )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
     )

    website_link = StringField(
        'website_link', validators=[URL()]
     )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
            'seeking_description'
    )

    def __init__(self, *args, **kwargs):
        super(ArtistForm, self).__init__(*args, **kwargs)
        states = db.session.scalars(sa.select(State)).all()
        self.state.choices = [(state.id, state.id) for state in states]
        genres = db.session.scalars(sa.select(Genre)).all()
        self.genres.choices = [(genre.id, genre.name) for genre in genres]