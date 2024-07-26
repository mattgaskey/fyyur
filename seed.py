from fyyur import create_app, db
from fyyur.models import State, Genre

def seed_states():
  states = [
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
  ]
  if not State.query.first():
    for id, name in states:
      new_state = State(id=id, name=name)
      db.session.add(new_state)

  db.session.commit()

def seed_genres():
  genres = [
    'Alternative',
    'Blues',
    'Classical',
    'Country',
    'Electronic',
    'Folk',
    'Funk',
    'Hip-Hop',
    'Heavy Metal',
    'Instrumental',
    'Jazz',
    'Musical Theatre',
    'Pop',
    'Punk',
    'R&B',
    'Reggae',
    'Rock n Roll',
    'Soul',
    'Other'
  ]
  if not Genre.query.first():
    for name in genres:
      new_genre = Genre(name=name)
      db.session.add(new_genre)
  
  db.session.commit()

if __name__ == '__main__':
  app = create_app()
  with app.app_context():
    seed_states()
    seed_genres()