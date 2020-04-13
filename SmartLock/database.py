from . import db
from flask_login import UserMixin
from flask import flash

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
    sensitivity = db.Column(db.String(45))
    associated_user = db.Column(db.String(45))
    
    def __repr__(self):
        return self.username

#this is the model for the rpi table in the db -jared
class Rpi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(45))
    pin_code = db.Column(db.String(45))
    active = db.Column(db.Boolean(1))
    user_id = db.Column(db.Integer())
    ip = db.Column(db.String(45))

    def __repr__(self):
        return self.id

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
def query_user_by_id(ref):
    return User.query.filter_by(id = ref).first()
    
#Query User By Email
def query_userByEmail(rEmail):
    return User.query.filter_by(email = rEmail).first()
#Create user call api - Adrian
def create_user(usr):
    try:
        db.session.add(usr)
        db.session.commit()
    except:
        flash('Error Adding User', 'error')
        db.session.rollback()

def delete_user(username):
    try:
        usr = user_query(username)
        db.session.delete(usr)
        db.session.commit()
    except:
        flash('Error Deleting User', 'error')
        db.session.rollback()

def create_entry_log(entry_log):
    try:
        db.session.add(entry_log)
        db.session.commit()
    except:
        db.session.rollback()

#creates an RPI Object
def create_rpi(rpi):
    try:
        db.session.add(rpi)
        db.session.commit()
    except:
        db.session.rollback()

#change user password
def update_pass(usrname, password):
    try:
        usr = user_query(usrname)
        usr.password = password
        db.session.commit()
        flash('Password Successful Changed', 'success')
    except:
        db.session.rollback()

#get all associated members
def get_members(usr_id):
    return User.query.filter_by(associated_user = str(usr_id)).all()

#Update pi's password - Adrian
def update_pi(sn, pin_code):
    try:
        pi = query_rpi(sn)
        pi.pin_code = pin_code
        db.session.commit()
    except:
        db.session.rollback()

#Queries pi - Adrian
def query_rpi(sn):
    return Rpi.query.filter_by(serial_number = sn).first()

#Queries pi - Adrian
def query_rpi_by_id(id):
    return Rpi.query.filter_by(user_id = id).first()

#Changes the user to verified=true -brandon (referenced from Adrian&Jared)
#Modified by Adrian
def verify_user(usr):
    try:
        usr.verified = True
        db.session.commit()
    except:
        db.session.rollback()

#Changes the rpi status -jared (referenced from Adrian)
#Modified by Adrian
def activate_pi(sn, stat):
    try:
        pi = Rpi.query.filter_by(serial_number=sn).first()
        pi.active = stat
        db.session.commit()
    except:
        db.session.rollback()

#Sets the IP Address of the device - Adrian
def setIp(sn, ip):
    try:
        pi = Rpi.query.filter_by(serial_number=sn).first()
        pi.ip = ip
        db.session.commit()
    except:
        db.session.rollback()

#Updates the rpi user_id
def rpi_user(serial_number, usr_id):
    try:
        rpi = Rpi.query.filter_by(serial_number = serial_number).first()
        rpi.user_id = usr_id
        db.session.commit()
    except:
        db.session.rollback()

#Queries user pincode  -jared
#Modified by Adrian
def query_pin_code(sn):
    rpi = query_rpi(sn)
    return rpi.pin_code 

#Queries rpi pin code by usr association
def get_mobile_information(user):
    usr = user_query(user)
    data = ''
    if usr.role == 'Linked-Member':
        owner = query_user_by_id(usr.associated_user)
        pi = Rpi.query.filter_by(user_id = owner.id).first()
        data = pi.pin_code + ','+pi.ip+','+usr.sensitivity
    else:
        pi = Rpi.query.filter_by(user_id = usr.id).first()
        data = pi.pin_code + ','+pi.ip+','+usr.sensitivity
    return data

#sets the user's sensitivity for the mobile app
def setSensitivity(user, sensitivity):
    try:
        usr = user_query(user)
        usr.sensitivity = sensitivity
        db.session.commit()
    except:
        db.session.rollback()
