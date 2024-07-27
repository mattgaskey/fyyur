from flask import render_template, request, flash, redirect, url_for, current_app
import sqlalchemy as sa
from fyyur import db
from fyyur.artist import bp
from fyyur.artist.forms import ArtistForm
from fyyur.models import Artist, City, Genre

@bp.route('/artists')
def artists():
  query = sa.Select(Artist).order_by(Artist.name)
  artists = db.session.scalars(query).all()
  data = []
  for artist in artists:
    data.append({
        "id": artist.id,
        "name": artist.name,
    })
  return render_template('pages/artists.html', artists=data)

@bp.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@bp.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  query = sa.select(Artist).where(Artist.id == artist_id)
  artist = db.session.scalar(query)
  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }
  
  return render_template('pages/show_artist.html', artist=artist)

@bp.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = db.session.scalar(sa.select(Artist).where(Artist.id == artist_id))
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.image_link.data = artist.image_link
  form.facebook_link.data = artist.facebook_link
  form.website_link.data = artist.website_link
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description
  form.genres.data = artist.genre_ids

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@bp.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm()
  if form.validate_on_submit():
      try:
          city_name = form.city.data
          state_id = form.state.data
          city = db.session.scalar(sa.select(City).where(City.name == city_name, City.state_id == state_id))
          if not city:
              city = City(name=city_name, state_id=state_id)
              db.session.add(city)
              db.session.commit()
          artist = db.session.scalar(sa.select(Artist).where(Artist.id == artist_id))
          artist.city_ref = city
          artist.name = form.name.data
          artist.phone = form.phone.data
          artist.image_link = form.image_link.data
          artist.facebook_link = form.facebook_link.data
          artist.website_link = form.website_link.data
          artist.seeking_venue = form.seeking_venue.data
          artist.seeking_description = form.seeking_description.data
          artist.clear_genres()

          for genre_id in form.genres.data:
              genre = db.session.scalar(sa.select(Genre).where(Genre.id == int(genre_id)))
              artist.add_genre(genre)
          db.session.commit()
          flash('Artist ' + request.form['name'] + ' was successfully updated!')
          current_app.logger.info(f"Artist {artist.name} successfully updated.")
      except Exception as e:
          db.session.rollback()
          flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
          current_app.logger.error(f"Error occurred while updating artist: {e}")
      finally:
          db.session.close()
  else:
      flash(request.form)
      flash(form.errors)
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated due to validation errors.')

  return redirect(url_for('artist.show_artist', artist_id=artist_id))

@bp.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@bp.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  if form.validate_on_submit():
      try:
          city_name = form.city.data
          state_id = form.state.data
          city = db.session.scalar(sa.select(City).where(City.name == city_name, City.state_id == state_id))
          if not city:
              city = City(name=city_name, state_id=state_id)
              db.session.add(city)
              db.session.commit()
          new_artist = Artist(
              name=form.name.data,
              city_ref=city,
              phone=form.phone.data,
              image_link=form.image_link.data,
              facebook_link=form.facebook_link.data,
              website_link=form.website_link.data,
              seeking_venue=form.seeking_venue.data,
              seeking_description=form.seeking_description.data
          )
          db.session.add(new_artist)
          db.session.flush()

          for genre_id in form.genres.data:
              genre = db.session.scalar(sa.select(Genre).where(Genre.id == int(genre_id)))
              new_artist.add_genre(genre)
          db.session.commit()
          flash('Artist ' + request.form['name'] + ' was successfully listed!')
          current_app.logger.info(f"Artist {new_artist.name} successfully created.")
      except Exception as e:
          db.session.rollback()
          flash(f'An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
          current_app.logger.error(f"Error occurred while creating artist: {e}")
      finally:
          db.session.close()
          artist_id = new_artist.id
  else:
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed due to validation errors.')

  return redirect(url_for('artist.show_artist', artist_id=artist_id))

@bp.route('/artists/<artist_id>/delete', methods=['POST'])
def delete_artist(artist_id):
  if request.form.get('_method') == 'DELETE':
    artist = db.session.scalar(sa.select(Artist).where(Artist.id == artist_id))
    try:
      db.session.delete(artist)
      db.session.commit()
      flash('Artist ' + artist.name + ' was successfully deleted!')
      current_app.logger.info(f"Artist {artist.name} successfully deleted.")
    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Artist ' + artist.name + ' could not be deleted.')
      current_app.logger.error(f"Error occurred while deleting artist: {e}")
    finally:
      db.session.close()
    return redirect(url_for('main.index'))
