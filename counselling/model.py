from flask_login import UserMixin
from datetime import  datetime
from flask_login import  current_user
from counselling import db,bcrypt,login_manager
from flask import request


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), unique=False, nullable=False)
    last_name = db.Column(db.String(30), unique=False, nullable=False)
    mob_number = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(100),nullable=False,default ='default.jpg')
    aadhar_file = db.Column(db.String(100), nullable=True)
    ip_address = db.Column(db.String(100), unique=False, nullable=False)
    date_register = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Users('{self.first_name}','{self.email}','{self.image_file}')"


