from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

# This is a method that you will be able to call in the app.py file. It will allow you to initiate the connction to the database.
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    # This will create a new user in the db
    __tablename__ = 'user'
    
    username = db.Column(db.String(20), primary_key=True, unique=True, autoincrement=False)

    password = db.Column(db.String(), nullable=False)

    email = db.Column(db.String(50), unique=True, nullable=False)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Register a user, hashing their password."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        db.session.add(user)
        return user




