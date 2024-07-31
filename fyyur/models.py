from typing import List
from datetime import timezone, datetime
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from fyyur import db
from fyyur.search import add_to_index, remove_from_index, query_index

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

class SearchableMixin(object):
  @classmethod
  def get_searchable_fields(cls):
    return getattr(cls, '__searchable__', [])
  
  @classmethod
  def search(cls, expression):
    ids, total = query_index(cls.__tablename__.lower(), expression)
    if total == 0:
      return {}, 0
    when = []
    for i in range(len(ids)):
      when.append((ids[i], i))
    query = sa.select(cls).where(cls.id.in_(ids)).order_by(
      db.case(*when, value=cls.id))
    return db.session.scalars(query), total
  
  @classmethod
  def before_commit(cls, session):
    session._changes = {
      'add': list(session.new),
      'update': list(session.dirty),
      'delete': list(session.deleted)
    }

  @classmethod
  def after_commit(cls, session):
    for obj in session._changes['add']:
      if isinstance(obj, SearchableMixin):
        add_to_index(obj.__tablename__.lower(), obj)
    for obj in session._changes['update']:
      if isinstance(obj, SearchableMixin):
        add_to_index(obj.__tablename__.lower(), obj)
    for obj in session._changes['delete']:
      if isinstance(obj, SearchableMixin):
        remove_from_index(obj.__tablename__.lower(), obj)
    session._changes = None

  @classmethod
  def reindex(cls):
    for obj in db.session.scalars(sa.select(cls)):
      add_to_index(cls.__tablename__.lower(), obj)
  
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

class Venue(SearchableMixin, db.Model):
    __tablename__ = 'Venue'
    __searchable__ = ['name']

    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
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
      return list(db.session.scalars(sa.select(Show).filter(Show.venue_id == self.id, Show.start_time < sa.func.now())))

    def get_upcoming_shows(self):
      return list(db.session.scalars(sa.select(Show).filter(Show.venue_id == self.id, Show.start_time >= sa.func.now())))

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
            "start_time": show.start_time.isoformat()
        } for show in self.get_past_shows()],
        "upcoming_shows": [{
            "artist_id": show.artist.id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.isoformat()
        } for show in self.get_upcoming_shows()],
        "past_shows_count": self.get_past_shows_count(),
        "upcoming_shows_count": self.get_upcoming_shows_count()
    }

class Artist(SearchableMixin, db.Model):
    __tablename__ = 'Artist'
    __searchable__ = ['name']

    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(), index=True)
    phone: so.Mapped[str] = so.mapped_column(sa.String(120))
    image_link: so.Mapped[str] = so.mapped_column(sa.String(500))
    facebook_link: so.Mapped[str] = so.mapped_column(sa.String(120))
    website_link: so.Mapped[str] = so.mapped_column(sa.String(120))
    seeking_venue: so.Mapped[bool] = so.mapped_column(sa.Boolean())
    seeking_description: so.Mapped[str] = so.mapped_column(sa.String(500))
    city_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('City.id'))
    available_start_date: so.Mapped[sa.Date] = so.mapped_column(sa.Date, nullable=True)
    available_end_date: so.Mapped[sa.Date] = so.mapped_column(sa.Date, nullable=True)
    available_start_time: so.Mapped[sa.Time] = so.mapped_column(sa.Time, nullable=True)
    available_end_time: so.Mapped[sa.Time] = so.mapped_column(sa.Time, nullable=True)
    
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
      return list(db.session.scalars(sa.select(Show).filter(Show.artist_id == self.id, Show.start_time < sa.func.now())))

    def get_upcoming_shows(self):
      return list(db.session.scalars(sa.select(Show).filter(Show.artist_id == self.id, Show.start_time >= sa.func.now())))

    def get_past_shows_count(self):
      return len(self.get_past_shows())

    def get_upcoming_shows_count(self):
      return len(self.get_upcoming_shows())

    def serialize(self):
      def format_date(date):
        return date.isoformat() if date else None

      def format_time(time):
        return datetime.strptime(str(time), '%H:%M:%S').strftime('%I:%M %p') if time else None
    
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
            "start_time": show.start_time.isoformat()
        } for show in self.get_past_shows()],
        "upcoming_shows": [{
            "venue_id": show.venue.id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": show.start_time.isoformat()
        } for show in self.get_upcoming_shows()],
        "past_shows_count": self.get_past_shows_count(),
        "upcoming_shows_count": self.get_upcoming_shows_count(),
        "available_start_date": format_date(self.available_start_date),
        "available_end_date": format_date(self.available_end_date),
        "available_start_time": format_time(self.available_start_time),
        "available_end_time": format_time(self.available_end_time)
    }

class Show(db.Model):
    __tablename__ = 'Show'

    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    start_time: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, nullable=False)

    artist_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('Artist.id'), index=True)
    venue_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('Venue.id'), index=True)

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