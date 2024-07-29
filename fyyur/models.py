from typing import List
from datetime import timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from fyyur import db

venue_genres = sa.Table(
    'venue_genres',
    db.metadata,
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True)
)

artist_genres = sa.Table(
    'artist_genres',
    db.metadata,
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True)
)

class Venue(db.Model):
    __tablename__ = 'Venue'

    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(120))
    address: so.Mapped[str] = so.mapped_column(sa.String(120))
    phone: so.Mapped[str] = so.mapped_column(sa.String(120))
    image_link: so.Mapped[str] = so.mapped_column(sa.String(500))
    facebook_link: so.Mapped[str] = so.mapped_column(sa.String(120))
    website_link: so.Mapped[str] = so.mapped_column(sa.String(120))
    seeking_talent: so.Mapped[bool] = so.mapped_column(sa.Boolean())
    seeking_description: so.Mapped[str] = so.mapped_column(sa.String(500))

    city_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('City.id'))
    city_ref: so.Mapped['City'] = so.relationship('City', back_populates='venues')
    genre_list: so.Mapped[List['Genre']] = so.relationship('Genre', secondary=venue_genres, back_populates='venues')
    genres: AssociationProxy[List[str]] = association_proxy('genre_list', 'name')
    genre_ids: AssociationProxy[List[int]] = association_proxy('genre_list', 'id')
    shows: so.Mapped[List['Show']] = so.relationship('Show', back_populates='venue')

    @property
    def genres(self):
        return [genre.name for genre in self.genre_list]
    
    @property
    def genre_ids(self):
        return [str(genre.id) for genre in self.genre_list]
    
    @property
    def city(self):
      return self.city_ref.name
    
    @property
    def state(self):
      return self.city_ref.state_id

    def __repr__(self) -> str:
      return f'<Venue {self.name}>'

    def add_genre(self, genre):
        if not self.has_genre(genre):   
            self.genre_list.append(genre)
    
    def has_genre(self, genre):
        return genre in self.genre_list
    
    def clear_genres(self):
      self.genre_list.clear()
      db.session.commit()
    
    def get_past_shows(self):
      return db.session.query(Show).filter(Show.venue_id == self.id, Show.start_time < sa.func.now()).all()

    def get_upcoming_shows(self):
      return db.session.query(Show).filter(Show.venue_id == self.id, Show.start_time >= sa.func.now()).all()

    def get_past_shows_count(self):
      return len(self.get_past_shows())

    def get_upcoming_shows_count(self):
      return len(self.get_upcoming_shows())
    
    def serialize(self):
      return {
        "id": self.id,
        "name": self.name,
        "genres": self.genres,
        "address": self.address,
        "city": self.city,
        "state": self.state,
        "phone": self.phone,
        "website_link": self.website_link,
        "facebook_link": self.facebook_link,
        "seeking_talent": self.seeking_talent,
        "seeking_description": self.seeking_description,
        "image_link": self.image_link,
        "past_shows": [{
            "artist_id": show.artist.id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.astimezone(timezone.utc).isoformat()
        } for show in self.get_past_shows()],
        "upcoming_shows": [{
            "artist_id": show.artist.id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.astimezone(timezone.utc).isoformat()
        } for show in self.get_upcoming_shows()],
        "past_shows_count": self.get_past_shows_count(),
        "upcoming_shows_count": self.get_upcoming_shows_count()
    }

class Artist(db.Model):
    __tablename__ = 'Artist'

    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String())
    phone: so.Mapped[str] = so.mapped_column(sa.String(120))
    image_link: so.Mapped[str] = so.mapped_column(sa.String(500))
    facebook_link: so.Mapped[str] = so.mapped_column(sa.String(120))
    website_link: so.Mapped[str] = so.mapped_column(sa.String(120))
    seeking_venue: so.Mapped[bool] = so.mapped_column(sa.Boolean())
    seeking_description: so.Mapped[str] = so.mapped_column(sa.String(500))

    city_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('City.id'))
    city_ref: so.Mapped['City'] = so.relationship('City', back_populates='artists')
    genre_list: so.Mapped[List['Genre']] = so.relationship('Genre', secondary=artist_genres, back_populates='artists')
    genres: AssociationProxy[List[str]] = association_proxy('genre_list', 'name')
    genre_ids: AssociationProxy[List[int]] = association_proxy('genre_list', 'id')
    shows: so.Mapped[List['Show']] = so.relationship('Show', back_populates='artist')

    @property
    def genres(self):
        return [genre.name for genre in self.genre_list]
    
    @property
    def genre_ids(self):
        return [str(genre.id) for genre in self.genre_list]
    
    @property
    def city(self):
      return self.city_ref.name
    
    @property
    def state(self):
      return self.city_ref.state_id

    def __repr__(self) -> str:
      return f'<Artist {self.name}>'

    def add_genre(self, genre):
        if not self.has_genre(genre):   
            self.genre_list.append(genre)
    
    def has_genre(self, genre):
        return genre in self.genre_list
    
    def clear_genres(self):
      self.genre_list.clear()
      db.session.commit()

    def get_past_shows(self):
      return db.session.query(Show).filter(Show.artist_id == self.id, Show.start_time < sa.func.now()).all()

    def get_upcoming_shows(self):
      return db.session.query(Show).filter(Show.artist_id == self.id, Show.start_time >= sa.func.now()).all()

    def get_past_shows_count(self):
      return len(self.get_past_shows())

    def get_upcoming_shows_count(self):
      return len(self.get_upcoming_shows())

    def serialize(self):
      return {
        "id": self.id,
        "name": self.name,
        "genres": self.genres,
        "city": self.city,
        "state": self.state,
        "phone": self.phone,
        "website_link": self.website_link,
        "facebook_link": self.facebook_link,
        "seeking_venue": self.seeking_venue,
        "seeking_description": self.seeking_description,
        "image_link": self.image_link,
        "past_shows": [{
            "venue_id": show.venue.id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": show.start_time.astimezone(timezone.utc).isoformat()
        } for show in self.get_past_shows()],
        "upcoming_shows": [{
            "venue_id": show.venue.id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": show.start_time.astimezone(timezone.utc).isoformat()
        } for show in self.get_upcoming_shows()],
        "past_shows_count": self.get_past_shows_count(),
        "upcoming_shows_count": self.get_upcoming_shows_count()
    }

class Show(db.Model):
    __tablename__ = 'Show'

    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    start_time: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, nullable=False)

    artist_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('Artist.id'))
    venue_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('Venue.id'))

    artist: so.Mapped['Artist'] = so.relationship('Artist', back_populates='shows')
    venue: so.Mapped['Venue'] = so.relationship('Venue', back_populates='shows')
    
    def __repr__(self) -> str:
      return f'<Show {self.id}>'

class State(db.Model):
    __tablename__ = 'State'

    id: so.Mapped[str] = so.mapped_column(sa.String(2), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(120))
    
    cities: so.WriteOnlyMapped['City'] = so.relationship(
        back_populates='state', passive_deletes=True)
    
    def __repr__(self) -> str:
      return f'<State {self.id}>'

class City(db.Model):
    __tablename__ = 'City'

    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(120))
    state_id: so.Mapped[str] = so.mapped_column(sa.String(2), sa.ForeignKey('State.id'))
    
    state: so.Mapped['State'] = so.relationship('State', back_populates='cities')
    artists: so.WriteOnlyMapped['Artist'] = so.relationship('Artist', back_populates='city_ref')
    venues: so.WriteOnlyMapped['Venue'] = so.relationship('Venue', back_populates='city_ref')

    def __repr__(self) -> str:
      return f'<City {self.name}, {self.state_id}>'

class Genre(db.Model):
    __tablename__ = 'Genre'

    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(120))

    artists: so.WriteOnlyMapped['Artist'] = so.relationship('Artist', secondary=artist_genres, viewonly=True)
    venues: so.WriteOnlyMapped['Venue'] = so.relationship('Venue', secondary=venue_genres, viewonly=True)

    def __repr__(self) -> str:
      return f'<Genre {self.name}>'