from . import db
from flask_login import UserMixin

#this is the model for the user table in the db -jared
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45))
    password = db.Column(db.String(45))
    first_name = db.Column(db.String(45))#Adrian
    last_name = db.Column(db.String(45))#Adrian
    email = db.Column(db.String(45))#Adrian
    role = db.Column(db.String(45))#Adrian
    pin_code = db.Column(db.String(45))#Adrian
    
    def __repr__(self):
        return self.username

#this is the model for the rpi table in the db -jared
class RPI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.String(45))
    user_id = db.Column(db.String(45))

    def __repr__(self):
        return self.mac_address

#user_query returns the first instance of username that is found by query -jared
def user_query(usr):
    return User.query.filter_by(username = usr).first()

#get user by ID #Adrian
def user_id_query(id):
    return User.query.get(int(id))

#Create user call api - Adrian
def create_user(usr):
    db.session.add(usr)
    db.session.commit()