import sqlalchemy as sa
import sqlalchemy.orm as so
from fyyur import create_app, db
from fyyur.models import Venue, Artist, Show

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'sa': sa, 'so': so, 'Venue': Venue, 'Artist': Artist, 'Show': Show}