import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash, Blueprint
from flask_login import login_user, logout_user, login_required


#sets up the authenticator blueprint - Adrian
auth = Blueprint('auth', __name__)

#Standard login function that loads the index.html - Adrian
@auth.route('/login')
def login_index():
    return render_template('index.html')

#route for the login - Adrian
@auth.route('/login', methods=['POST'])
def login():
    #Authentication/Login Code Goes Here - Adrian
    return 'Log In'

@auth.route('/signup')
def signup_index():
    return 'sign up template'

@auth.route('/signup', methods=['POST'])
def signup():
    #Authentication Code Goes Here - Adrian
    return 'sign up'

#route to logout the user from the session - Adrian 
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Log Out'

    