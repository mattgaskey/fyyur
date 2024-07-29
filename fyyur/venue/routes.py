from flask import render_template, request, flash, redirect, url_for, current_app, jsonify
import sqlalchemy as sa
from fyyur import db
from fyyur.venue import bp
from fyyur.venue.forms import VenueForm
from fyyur.models import Venue, City, Genre


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
  if venue is None:
      flash(f'Venue with id {venue_id} not found.')
      return redirect(url_for('main.index'))
  
  venue = venue.serialize()
 
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