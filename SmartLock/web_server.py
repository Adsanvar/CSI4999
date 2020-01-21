import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash, Blueprint
#from authenticator import auth
from flask_login import login_user, logout_user, login_required
from . import db

home = Blueprint('home', __name__)

#This Route is the index page (landing page) -Adrian
@home.route('/', methods=['GET'])
def index(): 
    return render_template('index.html')
   
#This routes is the dashboard page -Adrian
@home.route('/dashboard')
@login_required
def dashboard():
    return 'Dashboard' 

# #Main function that executes the application -Adrian
# if __name__ == '__main__':
#     #runs the flask application using an IP Address, Debug set to true so test the site and modify on the fly
#     app.run(debug=True)

