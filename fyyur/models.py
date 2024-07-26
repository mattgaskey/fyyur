import sqlalchemy as sa
import sqlalchemy.orm as so
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
    city: so.Mapped['City'] = so.relationship('City', back_populates='venues')
    genres: so.WriteOnlyMapped['Genre'] = so.relationship(
      secondary=venue_genres,
      primaryjoin=(venue_genres.c.venue_id == id),
      foreign_keys=[venue_genres.c.venue_id, venue_genres.c.genre_id])

    def __repr__(self) -> str:
      return f'<Venue {self.name}>'

    def add_genre(self, genre):
      if not self.has_genre(genre):   
        self.genres.add(genre)
    
    def has_genre(self, genre):
      query = self.genres.select().where(Genre.id == genre.id)
      return db.session.scalar(query) is not None

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
    city: so.Mapped['City'] = so.relationship('City', back_populates='artists')
    genres: so.WriteOnlyMapped['Genre'] = so.relationship(
      secondary=artist_genres,
      primaryjoin=(artist_genres.c.artist_id == id),
      foreign_keys=[artist_genres.c.artist_id, artist_genres.c.genre_id])

    def __repr__(self) -> str:
      return f'<Artist {self.name}>'

    def add_genre(self, genre):
      if not self.has_genre(genre):   
        self.genres.add(genre)
    
    def has_genre(self, genre):
      query = self.genres.select().where(Genre.id == genre.id)
      return db.session.scalar(query) is not None

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
    artists: so.WriteOnlyMapped['Artist'] = so.relationship('Artist', back_populates='city')
    venues: so.WriteOnlyMapped['Venue'] = so.relationship('Venue', back_populates='city')

    def __repr__(self) -> str:
      return f'<City {self.name}, {self.state}>'

class Genre(db.Model):
    __tablename__ = 'Genre'

    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(120))

    artists: so.WriteOnlyMapped['Artist'] = so.relationship('Artist', secondary=artist_genres, viewonly=True)
    venues: so.WriteOnlyMapped['Venue'] = so.relationship('Venue', secondary=venue_genres, viewonly=True)

    def __repr__(self) -> str:
      return f'<Genre {self.name}>'