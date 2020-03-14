from . import db
from flask_login import UserMixin

#this is the model for the user table in the db -jared
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45))
    password = db.Column(db.String(100))
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
    user_id = db.Column(db.Integer())

    def __repr__(self):
        return self.serial_number

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

#Query User By Email
def query_userByEmail(rEmail):
    return User.query.filter_by(email = rEmail).first()

#Create user call api - Adrian
def create_user(usr):
    db.session.add(usr)
    db.session.commit()

def create_entry_log(entry_log):
    db.session.add(entry_log)
    db.session.commit()

#creates an RPI Object
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

def update_pi_active(serial_number, status):
    pi = RPI.query.filter_by(mac_address=serial_number).first()
    pi.active = status
    db.session.commit()

#Queries pi - Adrian
def query_rpi(sn):
    return RPI.query.filter_by(serial_number = sn).first()

#Changes the user to verified=true -brandon (referenced from Adrian&Jared)
#Modified by Adrian
def verify_user(usr):
    usr.verified = True
    db.session.commit()

#Changes the rpi status -jared (referenced from Adrian)
#Modified by Adrian
def activate_pi(sn, stat):
    pi = RPI.query.filter_by(serial_number=sn).first()
    pi.active = stat
    db.session.commit()

#Updates the rpi user_id
def rpi_user(serial_number, usr_id):
    rpi = RPI.query.filter_by(serial_number = serial_number).first()
    rpi.user_id = usr_id
    db.session.commit()

#Queries user pincode  -jared
#Modified by Adrian
def query_pin_code(sn):
    rpi = query_rpi(sn)
    return rpi.pin_code 
def query_rpi():
    return RPI.query.filter_by(id=1).first()

def query_rpi_serial_number(serial_number):
    return RPI.query.filter_by(mac_address=serial_number).first()
