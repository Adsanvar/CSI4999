import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash
from authenticator import auth
from flask_login import login_user, logout_user, login_required

#imports SQlAlchemy libraries -jared
from flask_sqlalchemy import SQLAlchemy

#Creates the application module to run upon running script -Adrian
app = Flask(__name__)
app.register_blueprint(auth) #registers the authenticator auth routing to this module - Adrian

#this attaches db to flask object app -jared
db = SQLAlchemy(app)

#this configures the databse for communication with flask -jared
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@localhost/smart_lock'

#this is the model for the user table in the db -jared
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45))
    password = db.Column(db.String(45))

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
    return User.query.filter_by(username = usersearch).first()

#This Route is the index page (landing page) -Adrian
@app.route('/', methods=['GET'])
def index(): 
    return render_template('index.html')
   
#This routes is the dashboard page -Adrian
@app.route('/dashboard')
@login_required
def dashboard():
    return 'Dashboard' 

#Main function that executes the application -Adrian
if __name__ == '__main__':
    #runs the flask application using an IP Address, Debug set to true so test the site and modify on the fly
    app.run(debug=True)

