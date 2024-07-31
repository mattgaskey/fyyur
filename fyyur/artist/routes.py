from flask import render_template, request, flash, redirect, url_for, current_app, g
import sqlalchemy as sa
from fyyur import db
from fyyur.artist import bp
from fyyur.artist.forms import ArtistForm, ArtistSearchForm
from fyyur.models import Artist, City, Genre

@bp.route('/artists')
def artists():
  form = ArtistSearchForm()
  query = sa.Select(Artist).order_by(Artist.name)
  artists = db.session.scalars(query).all()
  data = []
  for artist in artists:
    data.append({
        "id": artist.id,
        "name": artist.name,
    })
  return render_template(
     'pages/artists.html', 
     artists=data, 
     form=form, 
     placeholder='Search for an Artist', 
     endpoint='/artists/search')

@bp.route('/artists/search', methods=['GET'])
def search_artists():
  form = ArtistSearchForm()
  if not form.validate():
     return redirect(url_for('artist.artists'))
  artists, total = Artist.search(form.search_term.data)
  response={
    "count": total,
    "data": artists
  }
  return render_template(
    'pages/search_artists.html', 
    results=response, 
    search_term=form.search_term.data,
    form=form, 
    placeholder='Search for an Artist', 
    endpoint='/artists/search')

@bp.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  query = sa.select(Artist).where(Artist.id == artist_id)
  artist = db.session.scalar(query)
  if not artist:
    flash('Artist not found.')
    return redirect(url_for('main.index'))
  artist = artist.serialize()
  
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
  artist = db.session.scalar(sa.select(Artist).where(Artist.id == artist_id))

  if form.validate_on_submit():
      try:
          city_name = form.city.data
          state_id = form.state.data
          city = db.session.scalar(sa.select(City).where(City.name == city_name, City.state_id == state_id))
          if not city:
              city = City(name=city_name, state_id=state_id)
              db.session.add(city)
              db.session.commit()
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
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated due to validation errors.')
      return render_template('forms/edit_artist.html', form=form, artist=artist)

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
      return render_template('forms/new_artist.html', form=form)
  if artist_id:
    return redirect(url_for('artist.show_artist', artist_id=artist_id))
  else:
    return redirect(url_for('main.index'))

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
