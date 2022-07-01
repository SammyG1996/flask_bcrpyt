from models import db, User
from app import app

# create all tables
db.drop_all()
db.create_all()

# If table isnt empty then empty it
User.query.delete()

db.session.commit()