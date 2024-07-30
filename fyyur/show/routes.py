from flask import render_template, flash, redirect, url_for, current_app
import sqlalchemy as sa
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
      "start_time": show.start_time
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
      show = Show(
        artist_id=form.artist_id.data,
        venue_id=form.venue_id.data,
        start_time=form.start_time.data
      )
      db.session.add(show)
      db.session.commit()
      flash('Show was successfully listed!')
    except Exception as e:
      db.session.rollback()
      flash(f'An error occurred. Show could not be listed.')
      current_app.logger.error(f"Error occurred while creating venue: {e}")
    finally:
      db.session.close()
  else:
    flash(form.errors)
    flash('An error occurred. Show could not be updated due to validation errors.')
  return redirect(url_for('show.shows'))