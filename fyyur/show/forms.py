from flask import render_template, flash
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField
from wtforms.validators import DataRequired, ValidationError
import sqlalchemy as sa
from fyyur import db
from fyyur.models import Artist, Venue

class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id',
        validators=[DataRequired()]
    )
    venue_id = StringField(
        'venue_id',
        validators=[DataRequired()]
    )
    start_time = DateTimeField(
        'start_time',
        format='%Y-%m-%d %I:%M %p',
        validators=[DataRequired()],
        default=datetime.today()
    )

    def validate_artist_id(self, artist_id):
      artist = db.session.scalar(sa.select(Artist).where(Artist.id == artist_id.data))
      if not artist:
        raise ValidationError('Artist does not exist.')
    
    def validate_venue_id(self, venue_id):
      venue = db.session.scalar(sa.select(Venue).where(Venue.id == venue_id.data))
      if not venue:
        raise ValidationError('Venue does not exist.')