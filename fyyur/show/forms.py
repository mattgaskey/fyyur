from flask import render_template, flash
from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import SelectField, DateTimeLocalField
from wtforms.validators import DataRequired
import sqlalchemy as sa
from fyyur import db
from fyyur.models import Artist, Venue

class ShowForm(FlaskForm):
    artist_id = SelectField(
        'artist_id',
        validators=[DataRequired()],
        choices=[]
    )
    venue_id = SelectField(
        'venue_id',
        validators=[DataRequired()],
        choices=[]
    )
    start_time = DateTimeLocalField(
        'start_time',
        format='%Y-%m-%dT%H:%M',
        validators=[DataRequired()],
        default=datetime.now()
    )

    def __init__(self, *args, **kwargs):
      super(ShowForm, self).__init__(*args, **kwargs)
      artists = db.session.scalars(sa.select(Artist).order_by(Artist.name)).all()
      self.artist_id.choices = [(artist.id, artist.name) for artist in artists] if artists else [('', 'No artist available')]
      venues = db.session.scalars(sa.select(Venue).order_by(Venue.name)).all()
      self.venue_id.choices = [(venue.id, f"{venue.name} - {venue.city}, {venue.state}") for venue in venues] if venues else [('', 'No venue available')]