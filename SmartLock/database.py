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
    verified = db.Column(db.Boolean(1))#brandons
    def __repr__(self):
        return self.username

#this is the model for the rpi table in the db -jared
class RPI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(45))
    pin_code = db.Column(db.String(45))
    active = db.Column(db.Boolean(1))


    def __repr__(self):
        return self.mac_address

class Entry_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String(45))
    entry_type = db.Column(db.String(45))
    user = db.Column(db.String(45))

    def __repr__(self):
        return self.id

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

def create_entry_log(entry_log):
    db.session.add(entry_log)
    db.session.commit()

def create_rpi(rpi):
    db.session.add(rpi)
    db.session.commit()

def update_pass(usr, password):
    usr.password = password
    db.session.commit()

#Update pi's password - Adrian
def update_pi(pi, pin_code):
    pi.pin_code = pin_code
    db.session.commit()

#Queries pi - Adrian
def query_rpi():
    return RPI.query.filter_by(id=1).first()
#Queries User- Brandon
def query_user():
    return User.query.filter_by(id=1).first()