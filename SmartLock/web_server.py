import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for
#from authenticator import auth
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from SmartLock.database import user_query, create_entry_log, Entry_log

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
    #details = 'User: ' + current_user.username + '\nRole: ' + current_user.role
    #return render_template('dashboard.html', info = details)
    return render_template('pinpad.html')
    
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
    return render_template('pinpad_test.html') 

#This route is the keypad landing page for post commands
@home.route("/keypad", methods=['POST'])
@login_required
def post_keypad():
    #Jared
    #if keypad enter button is pressed
    if 'submitpin' in request.form:
        #TODO error detection for keypad inputs to be entered here

        #scrape input from the pin textbox
        pin = request.form.get('userpin')

        #this code is not being used...
        #set a new instance variable usr to the one already
        #created in the authenticator class under the login method
        #usr = login.usr

        #if no input is detected
        if pin == None:
            return redirect(url_for('home.keypad'))
        else:
            #authenticate entered pin with the pin code in the db
            if pin == current_user.pin_Code:
                #open door
                #TODO interface code between rpi and door lock
                print('It\'s working!')
                return redirect(url_for('home.keypad'))
            else:
                return redirect(url_for('home.keypad'))
    else:
        return redirect(url_for('home.keypad'))

