from flask import render_template, request, flash, redirect, url_for, current_app
import sqlalchemy as sa
from fyyur import db
from fyyur.venue import bp
from fyyur.venue.forms import VenueForm
from fyyur.models import Venue, City, State, Genre

@bp.route('/venues')
def venues():
  query = sa.select(City).order_by(City.state_id, City.name)
  locations = db.session.scalars(query).all()
  data = []
  for location in locations:
    if db.session.scalar(sa.select(Venue).where(Venue.city_id == location.id)):
      data.append({
          "city": location.name,
          "state": location.state_id,
          "venues": db.session.scalars(
             sa.select(Venue).where(Venue.city_id == location.id).order_by(Venue.name)).all()
      })
 
  return render_template('pages/venues.html', areas=data);

@bp.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@bp.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  query = sa.select(Venue).where(Venue.id == venue_id)
  venue = db.session.scalar(query)
  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
 
  return render_template('pages/show_venue.html', venue=venue)


@bp.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@bp.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  if form.validate_on_submit():
      try:
          city_name = form.city.data
          state_id = form.state.data
          city = db.session.scalar(sa.select(City).where(City.name == city_name, City.state_id == state_id))
          if not city:
              city = City(name=city_name, state_id=state_id)
              db.session.add(city)
              db.session.commit()
          new_venue = Venue(
              name=form.name.data,
              city_ref=city,
              address=form.address.data,
              phone=form.phone.data,
              image_link=form.image_link.data,
              facebook_link=form.facebook_link.data,
              website_link=form.website_link.data,
              seeking_talent=form.seeking_talent.data,
              seeking_description=form.seeking_description.data
          )
          db.session.add(new_venue)
          db.session.flush()

          for genre_id in form.genres.data:
              genre = db.session.scalar(sa.select(Genre).where(Genre.id == int(genre_id)))
              print(genre)
              new_venue.add_genre(genre)
          db.session.commit()
          flash('Venue ' + request.form['name'] + ' was successfully listed!')
          current_app.logger.info(f"Venue {new_venue.name} successfully created.")
      except Exception as e:
          db.session.rollback()
          flash(f'An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
          current_app.logger.error(f"Error occurred while creating venue: {e}")
      finally:
          db.session.close()
          venue_id = new_venue.id
  else:
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed due to validation errors.')

  return redirect(url_for('venue.show_venue', venue_id=venue_id))

@bp.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = db.session.scalar(sa.select(Venue).where(Venue.id == venue_id))
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.image_link.data = venue.image_link
  form.genres.data = venue.genre_ids
  form.facebook_link.data = venue.facebook_link
  form.website_link.data = venue.website_link
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@bp.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm()
  if form.validate_on_submit():
    try:
      city_name = form.city.data
      state_id = form.state.data
      city = db.session.scalar(sa.select(City).where(City.name == city_name, City.state_id == state_id))
      if not city:
          city = City(name=city_name, state_id=state_id)
          db.session.add(city)
          db.session.commit()
      venue = db.session.scalar(sa.select(Venue).where(Venue.id == venue_id))
      
      venue.name=form.name.data
      venue.city_ref=city
      venue.address=form.address.data
      venue.phone=form.phone.data
      venue.image_link=form.image_link.data
      venue.facebook_link=form.facebook_link.data
      venue.website_link=form.website_link.data
      venue.seeking_talent=form.seeking_talent.data
      venue.seeking_description=form.seeking_description.data
      venue.clear_genres()

      for genre_id in form.genres.data:
          genre = db.session.scalar(sa.select(Genre).where(Genre.id == int(genre_id)))
          venue.add_genre(genre)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully updated!')
      current_app.logger.info(f"Venue {venue.name} successfully updated.")
    except Exception as e:
      db.session.rollback()
      flash(f'An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
      current_app.logger.error(f"Error occurred while creating venue: {e}")
    finally:
      db.session.close()
  else:
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated due to validation errors.')
        
  return redirect(url_for('venue.show_venue', venue_id=venue_id))

@bp.route('/venues/<venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):
  if request.form.get('_method') == 'DELETE':
    venue = db.session.scalar(sa.select(Venue).where(Venue.id == venue_id))
    try:
      db.session.delete(venue)
      db.session.commit()
      flash('Venue ' + venue.name + ' was successfully deleted!')
      current_app.logger.info(f"Venue {venue.name} successfully deleted.")
    except Exception as e:
      db.session.rollback()
      flash('An error occurred. Venue ' + venue.name + ' could not be deleted.')
      current_app.logger.error(f"Error occurred while deleting venue: {e}")
    finally:
      db.session.close()
    return redirect(url_for('main.index'))