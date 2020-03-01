#import os, threading, webbrowser, subprocess
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

@auth.route('/signupUserError/<info>', methods = ['GET'])
def signupUserError(info):
    first = info[0]
    last = info[1]
    email = info[2]
    serial = info[3]
    error = info[4]
    return render_template('signup.html', firstname = first, info = error)

#route for the sign up post command - Adrian
@auth.route('/signup', methods=['POST'])
def signup():
    #Authentication Code Goes Here - Adrian

    #checks to see if the the username field is empty -Adrian
    if request.form.get('signup_username') and request.form.get('signup_password') and request.form.get('firstname') and request.form.get('lastname') and request.form.get('email') and request.form.get('serial_num'):
        #Non-empty
        uname = request.form.get('signup_username')
        pas = request.form.get('signup_password')
        name = request.form.get('firstname')
        last = request.form.get('lastname')
        mail = request.form.get('email')
        serial = request.form.get('serial_num')
        
        test = database.user_query(uname)
        
        #check to make sure the user is unique -Adrian
        if database.user_query(uname) == None:
            print("IN HERE")
            #obtaines user from database thru ORM
            # usr = database.User(username=uname, password = pas, first_name=name, last_name=last, role='Member', email=mail, verified = False)
            # database.create_user(usr)
            return redirect(url_for('auth.login'))
        else:
            lst = []
            lst.append(name)
            lst.append(last)
            lst.append(mail)
            lst.append(serial)
            return redirect(url_for('auth.signupUserError'))

        
    else:
        #empty
        return redirect(url_for('auth.signup'))
#Route for changing User Password
@auth.route('/verification/<key>', methods=['GET'])
def verification(key):
    check = database.query_user(username=key)
    if check == None:
        return redirect(url_for('index.html'))
    else: 
        database.verification(key, True)
        return redirect(url_for('auth.login'))

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

#Route to set active status -jared (referenced from Adrian)
@auth.route('/setActive/<sn>', methods=['GET'])
def setActive(sn):
    database.active_status(sn, True)
    return "Success"

#Route to get pi information and update rpi pincode if certain
#verification checks are met -jared (referenced from Adrian)
@auth.route('/getPiInformation/<sn>', methods=['GET'])
def getPiInformation(sn):
    rpi = database.query_serial(sn)
    user = database.query_user()
    if rpi.serial_number == None or rpi.active == False:
        return "404"
    elif rpi.serial_number != None and rpi.active != False:
        #if initial check of sn and status is successful,
        # check for verification in the rpi db -jared
        if user.verified == 0:
            return "404"
        elif user.verified == 1:
            #if user is verified, retrieve the pin code from the
            #user table in the remote db and copy to the rpi db -jared
            copied_pin = database.query_pin_code(sn)
            rpi.pin_code = copied_pin
            db.session.commit()
            return 'RPI initialized'

#check if the serial number is active or not
def checkActive(serial_number):
    try:
        #query rpi table
        
        return True 
    except:
        return False

 #sends mail to the intended user
def sendMail(to, subject ,message):
    try:
        import smtplib
        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()

        s.login("smartlock.noreply@gmail.com", "TESt123!")
        
        s.sendmail("pitest873@gmail.com", to, message)

        s.quit()

    except:
        raise