import sqlalchemy as sa
import sqlalchemy.orm as so
from fyyur import db, current_app

class Venue(db.Model):
    __tablename__ = 'Venue'

    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(120))
    city: so.Mapped[str] = so.mapped_column(sa.String(120))
    state: so.Mapped[str] = so.mapped_column(sa.String(120))
    address: so.Mapped[str] = so.mapped_column(sa.String(120))
    phone: so.Mapped[str] = so.mapped_column(sa.String(120))
    image_link: so.Mapped[str] = so.mapped_column(sa.String(500))
    facebook_link: so.Mapped[str] = so.mapped_column(sa.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id: so.Mapped[int] = so.mapped_column(sa.Integer(), primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String())
    city: so.Mapped[str] = so.mapped_column(sa.String(120))
    state: so.Mapped[str] = so.mapped_column(sa.String(120))
    phone: so.Mapped[str] = so.mapped_column(sa.String(120))
    genres: so.Mapped[str] = so.mapped_column(sa.String(120))
    image_link: so.Mapped[str] = so.mapped_column(sa.String(500))
    facebook_link: so.Mapped[str] = so.mapped_column(sa.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
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
    
    state: so.Mapped[State] = so.relationship(back_populates='cities')

    def __repr__(self) -> str:
      return f'<City {self.name}, {self.state}>'