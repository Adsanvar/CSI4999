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
                else:
                    return redirect(url_for('auth.login'))
        else:
            #empty
            return redirect(url_for('auth.login'))
            
    #if signup button clicked send to signup page        
    if 'signup' in request.form:
        return redirect(url_for('auth.signup'))

#Route for changing RPI Password
@auth.route('/rpi/<pas>')
def rpi_config(pas):
    rpi = database.query_rpi()
    database.update_pi(rpi, pas)

    return redirect(url_for('home.dashboard'))

