'''bycrypt Application'''

from crypt import methods
from dataclasses import dataclass
from flask import Flask, redirect, render_template, session
from secret import secret_key
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddRegisterForm, LoginForm
from flask_bcrypt import Bcrypt
from werkzeug.exceptions import Unauthorized


# this is initiate the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = secret_key

debug = DebugToolbarExtension(app)


bcrypt = Bcrypt()


# this will connect the app to the DB
connect_db(app)

@app.route('/')
def homepage():
  '''This will contain all the pets that are currently posted on the application'''
  return redirect('/register')
  

@app.route('/register', methods=['POST', 'GET'])
def register():
  '''This will contain all the pets that are currently posted on the application'''
  form = AddRegisterForm()
  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    email = form.email.data
    first_name = form.first_name.data
    last_name = form.last_name.data

    user = User.register(username, password, first_name, last_name, email)

    db.session.commit()
    session['username'] = user.username

    return redirect(f'/users/{session["username"]}')
  
  else:
    return render_template('register.html', form = form, 
    )


# This will allow the user to loggin
@app.route('/login', methods=['POST', 'GET'])
def login():
  form = LoginForm()

  if form.validate_on_submit():
    username = User.query.get(form.username.data)
    stored_pw = form.password.data
    
    # Check to see if username and PW 
    # Match the DB and then redirect to secrets

    # bcrypt.check_password_hash(username.password, form.password.data)

    if username and bcrypt.check_password_hash(username.password, stored_pw):
      session['username'] = username.username
      return redirect(f'/users/{username.username}')
    else:
      # ADD A Flask Flash Method
      return render_template('login.html', form = form, session = session)
  elif "username" in session:
    return redirect(f"/users/{session['username']}")
  else:
    return render_template('login.html', form = form, session = session)




# This will let you log out
@app.route("/logout")
def logout():
    """Logout route."""
    if "username" in session:
      session.pop("username")
      
    return redirect("/login")

# redirects users that are not logged in
@app.route("/users/")
def redirect_user():

    return redirect("/login")


@app.route("/users/<username>")
def show_user(username):
    """Example page for logged-in-users."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()
    user = User.query.get(username)

    return render_template("users_show.html", user=user, session = session)


@app.route('/users/<user>/delete', methods=['POST'])
def delete_user(user):
  '''This route will is a POST request that will delete the selcted user. '''
  if "username" in session:
    User.query.filter_by(username=user).delete()
    db.session.commit()
    session.pop("username")

    return redirect('/register')

  else:
    return redirect('/login')
