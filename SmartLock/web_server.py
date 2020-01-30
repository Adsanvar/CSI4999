import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for
#from authenticator import auth
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from SmartLock.database import user_query

home = Blueprint('home', __name__)

#This Route is the index page (landing page) -Adrian
@home.route('/', methods=['GET'])
def index(): 
    return render_template('index.html')
   
#This routes is the dashboard page -Adrian
@home.route('/dashboard')
@login_required
def dashboard():
    #displays details of user in dashboard
    details = 'User: ' + current_user.username + '\nRole: ' + current_user.role
    return render_template('dashboard.html', info = details)

#This routes is the dashboard post page to handle post commands inside the dashboard web page -Adrian
@home.route('/dashboard', methods=['POST'])
@login_required
def post_dashboard():
    #if the log out button is clicked 
    if 'logout' in request.form:
        return redirect(url_for('auth.logout'))

#This route is the keypad page
@home.route("/keypad")
@login_required
def keypad():
    #TODO: Update to the proper keypad.html file
    return render_template('index.html') 

#This route is the keypad landing page for post commands
@home.route("/keypad", methods=['POST'])
@login_required
def post_keypad():
    #TODO: Need to implement keypad stuff
    return redirect(url_for('home.keypad'))

