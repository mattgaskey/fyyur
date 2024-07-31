from flask import render_template, flash, redirect, url_for, current_app
import sqlalchemy as sa
from datetime import time
from fyyur import db
from fyyur.show import bp
from fyyur.show.forms import ShowForm
from fyyur.models import Show, Artist, Venue

@bp.route('/shows')
def shows():
  query = db.session.scalars(sa.Select(Show).join(Artist).join(Venue).order_by(Show.start_time))
  data = []
  for show in query:
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.isoformat()
    })
  return render_template('pages/shows.html', shows=data)

@bp.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@bp.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm()
  if form.validate_on_submit():
    try:
      artist = db.session.scalar(sa.select(Artist).where(Artist.id == form.artist_id.data))
      start_time = form.start_time.data

      start_date = start_time.date()
      start_time_only = start_time.time()

      if artist.available_end_time == time(0, 0, 0):
        artist_end_time = time(23, 59, 59)
      else:
        artist_end_time = artist.available_end_time

      if (artist.available_start_date and start_date < artist.available_start_date) or \
         (artist.available_end_date and start_date > artist.available_end_date) or \
         (artist.available_start_time and start_time_only < artist.available_start_time) or \
         (artist_end_time and start_time_only > artist_end_time):
        flash(f'An error occurred. Show time is outside the artist\'s availability. Please check the artist\'s availability <a href="{url_for("artist.show_artist", artist_id=artist.id)}">here</a>.')
        return redirect(url_for('show.create_shows'))
      
      show = Show(
        artist_id=form.artist_id.data,
        venue_id=form.venue_id.data,
        start_time=start_time
      )
      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!')
    except Exception as e:
      db.session.rollback()
      flash(f'An error occurred. Show could not be listed. {str(e)}')
      current_app.logger.error(f"Error occurred while creating venue: {e}")
    finally:
      db.session.close()
  else:
    flash('An error occurred. Show could not be updated due to validation errors.')
  return redirect(url_for('show.shows'))