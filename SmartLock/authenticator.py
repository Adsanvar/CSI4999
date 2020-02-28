import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash, Blueprint, redirect, url_for
from flask_login import login_user, logout_user, login_required
from . import db
from SmartLock.database import User, create_user, user_query, update_pass
import SmartLock.database as database
##import RPI.GPIO as GPIO ##sam


##GPIO.setmode(GPIO.BCM) ##sam
##GPIO.setwarnings(False) ##sam
##GPIO.setup(18,GPIO.OUT) ##sam
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
            usr = user_query(name)
            #checks if usr returned is null if so redirect to the login
            if usr == None:
                return redirect(url_for('auth.login'))
            else:
                #authenticates user to db
                if usr.username == name and usr.password == pas:
                    #route to dashboard and update the login session
                    login_user(usr)
                    ##GPIO.output(18, GPIO.HIGH)
                    return redirect(url_for('home.dashboard'))
                else:
                    ##GPIO.output(18,GPIO.LOW) ##sam
                    return redirect(url_for('auth.login'))
                    
        else:
            #empty
            ##GPIO.cleanup() ##sam
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

        if database.user_query(uname) == None:
            #obtaines user from database thru ORM
            usr = User(username=uname, password = pas, first_name=name, last_name=last, role='Admin', email=mail)


                message = 'http://localhost:5000/' + uname
                subject = 'Email Verification'
                sendMail(mail, subject, message)
        else:
            #show the user that the Username is taken.
            print("Username Taken")
       
      
        return redirect(url_for('auth.login'))
    else:
        #empty
        return redirect(url_for('auth.signup'))

def checkActive(serial_number):
    try:
        #query rpi table
        return True 
    except:
        return False

def checkDatabase(user):
    try:
        create_user(usr)
        return True
    except:
        return False
 
def sendMail(to, subject ,message):
    try:
        import smtplib
        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()
        #Google how to add a subject to email using the smtplib library.
        s.login("pitest873@gmail.com", "TESt123!")
        
        s.sendmail("pitest873@gmail.com", to, message)

        s.quit()

    except:
        raise

#route to logout the user from the session - Adrian 
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))



