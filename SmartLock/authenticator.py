import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash, Blueprint, redirect, url_for
from flask_login import login_user, logout_user, login_required
from . import db
import SmartLock.database as database

#sets up the authenticator blueprint - Adrian
auth = Blueprint('auth', __name__)

#Standard login function that loads the index.html - Adrian
@auth.route('/login')
def login_index():
    return render_template('index.html')

#route for the login - Adrian
@auth.route('/login', methods=['POST'])
def login():
    #Adrian
    #if login button is activated proceed with authentication
    if 'login' in request.form:
        #checks to see if the the username field is empty
        if request.form.get('username'):
            #Non-empty
            name = request.form.get('username')
            pas = request.form.get('password')
            #obtaines user from database thru ORM
            usr = database.user_query(name)
            #checks if usr returned is null if so redirect to the login
            if usr == None:
                return redirect(url_for('auth.login'))
            else:
                #authenticates user to db
                if usr.username == name and usr.password == pas:
                    #Determines the role of the logged in user - Adrina
                    if usr.role == 'rpi':
                        login_user(usr) #if usr is rpi redirect them to the keypad route in web_server.py
                        return redirect(url_for('home.keypad'))
                    if usr.role == 'Admin': 
                        #route to dashboard and update the login session
                        login_user(usr)
                        #led.on()
                        return redirect(url_for('home.dashboard'))
                else:
                    return redirect(url_for('auth.login'))
        else:
            #empty
            return redirect(url_for('auth.login'))
            
    #if signup button clicked send to signup page        
    if 'signup' in request.form:
        return redirect(url_for('auth.signup'))


#route for the signup - Adrian
@auth.route('/signup')
def signup_index():
    return render_template('signup.html')

#route for the sign up post command - Adrian
@auth.route('/signup', methods=['POST'])
def signup():
    #Authentication Code Goes Here - Adrian

    #checks to see if the the username field is empty
    if request.form.get('signup_username') and request.form.get('signup_password') and request.form.get('firstname') and request.form.get('lastname') and request.form.get('email'):
        #Non-empty
        uname = request.form.get('signup_username')
        pas = request.form.get('signup_password')
        name = request.form.get('firstname')
        last = request.form.get('lastname')
        mail = request.form.get('email')
        #obtaines user from database thru ORM
        usr = database.User(username=uname, password = pas, first_name=name, last_name=last, role='Member', email=mail)
        database.create_user(usr)

        return redirect(url_for('auth.login'))
    else:
        #empty
        return redirect(url_for('auth.signup'))

#Route for changing RPI Password
@auth.route('/rpi/<pas>')
@login_required
def rpi_config(pas):
    print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('INIDE RPI'))

    rpi = database.query_rpi()
    database.update_pi(rpi, pas)

    print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('SUCCESS'))
    return redirect(url_for('home.dashboard'))

#Route for changing User Password
@auth.route('/userpass/<pas>')
@login_required
def userpass(pas):
    print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('INIDE User'))

    userpass = database.query_user()
    database.update_pass(userpass, pas)

    print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('SUCCESS'))
    return redirect(url_for('home.dashboard'))

#route to logout the user from the session - Adrian 
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))

