from flask import request, flash
from wtforms import StringField, SelectField, SelectMultipleField, BooleanField, DateField, TimeField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL, ValidationError, Optional
import phonenumbers, re
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
        'phone'
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    genres = SelectMultipleField(
      'genres', 
      validators=[DataRequired()],
      choices=[]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
     )

    website_link = StringField(
        'website_link', validators=[URL()]
     )

    seeking_venue = BooleanField( 
        'seeking_venue', validators=[Optional()] 
    )

    seeking_description = StringField(
            'seeking_description'
    )
    not_before_date = DateField(
        'not_before_date', validators=[Optional()]
    )
    not_after_date = DateField(
        'not_after_date', validators=[Optional()]
    )
    not_before_time = TimeField(
        'not_before_time', validators=[Optional()]
    )
    not_after_time = TimeField(
        'not_after_time', validators=[Optional()]
    )

    def __init__(self, *args, **kwargs):
        super(ArtistForm, self).__init__(*args, **kwargs)
        states = db.session.scalars(sa.select(State).order_by(State.name)).all()
        self.state.choices = [(state.id, state.id) for state in states]
        genres = db.session.scalars(sa.select(Genre)).all()
        self.genres.choices = [(genre.id, genre.name) for genre in genres]
    
    def validate_phone(form, field):
        phone_number = re.sub(r'\D', '', field.data)

        if len(phone_number) > 10:
            raise ValidationError('Invalid phone number. Please use a 10-digit US format.')
        try:
            input_number = phonenumbers.parse(phone_number)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number. Please use a 10-digit US format.')
        except:
            input_number = phonenumbers.parse('+1'+phone_number)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number. Please use a 10-digit US format.')

class ArtistSearchForm(FlaskForm):
    search_term = StringField(
        'search_term', validators=[DataRequired()]
    )

    def __init__(self, *args, **kwargs):
      if 'formdata' not in kwargs:
        kwargs['formdata'] = request.args
      if 'meta' not in kwargs:
        kwargs['meta'] = {'csrf': False}
      super(ArtistSearchForm, self).__init__(*args, **kwargs)