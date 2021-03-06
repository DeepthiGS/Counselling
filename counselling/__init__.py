from flask import Flask, render_template, flash,redirect,url_for
from flask_bcrypt import  Bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime
from flask_login import LoginManager



app = Flask(__name__)
app.config['SECRET_KEY'] = '374bef570b27058b66be0365a31a94c3'

local_server = False
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:12aer56uil90@localhost/counsell"
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://crttszlcbtfnte:1d78c500a199e2394e98c220b94311fcbc869ff3f681bb3c65f243370e9f3b3b@ec2-54-160-18-230.compute-1.amazonaws.com:5432/du3u2mt8n1fdc"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True





db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


# this is for the @login_reuired decorartor to understand to take to the login sceen if the user is not logged in and trying to access the accounts screen ,, after = wwe put the funtion name
login_manager.login_view = 'users.login'
# inorder to make our message of access dined in format of flsh meszage
login_manager.login_message_category = 'info'
