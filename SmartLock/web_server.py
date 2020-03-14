from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for
#from authenticator import auth
from flask_login import login_user, logout_user, login_required, current_user
from . import db
import SmartLock.database as database
#from gpiozero import LED
#from time import sleep

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
    details = current_user.username
    return render_template('dashboard.html', info = details)

#This routes is the dashboard post page to handle post commands inside the dashboard web page -Adrian
@home.route('/dashboard', methods=['POST'])
@login_required
def post_dashboard():
    #if the log out button is clicked 
    if 'logout' in request.form:
        return redirect(url_for('auth.logout'))
    if 'confirm1' in request.form: #if confirm button is clicked the dashboard
        #obtain input
        old_pin = request.form.get('old_rpi_password')

        rpi = database.query_rpi()

        if old_pin == rpi.pin_code : #make sure they match, redirect to rpi_config with pas as a parameter - Adrian
            new_pin = request.form.get('rpi_password')
            confrim_pin = request.form.get('rpi_confirm_password')
            if new_pin == confrim_pin:
                print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('PIN confirmed'))
                return redirect(url_for('auth.rpi_config', pas=confrim_pin))
            else:
                print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('Confirmation Failed'))
                return redirect(url_for('home.dashboard'))
        else: #if failed redirect to dashboard
            print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('pass not confirmed'))
            return redirect(url_for('home.dashboard'))
  
    #if confirm button is activated proceed with change of password
    if 'confirm2' in request.form:
        old_pass = request.form.get('old_password')

        userpass = database.query_user()
        if old_pass == userpass.password:
            #checks to see if the inputed password is the same as the one in database
            if request.form.get('original_password') != request.form.get('new_password'): 
                #user can not change password to same password
                if old_pass == userpass.password : 
                    #make sure they match database, redirect to userpass with pas as a parameter - Brandon
                    new_pass = request.form.get('new_password')
                    confrim_pass = request.form.get('confirm_password')
                    if new_pass == confrim_pass:
                        print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('Password confirmed'))
                        return redirect(url_for('auth.userpass', pas=confrim_pass))
                    else:
                        print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('Confirmation Failed'))
                        return redirect(url_for('home.dashboard'))
                else: #if failed redirect to dashboard
                    print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('Password was not confirmed'))
                    return redirect(url_for('home.dashboard'))
            else:#if failed redirect to dashboard
                flash('Password will not be changed')
                return redirect(url_for('home.dashboard'))
        else:#empty  
            flash('Every input is required')
            return redirect(url_for('home.dashboard'))

#This route is the keypad page - Adrian
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
        print('IN SUBMIT')
        #scrape input from the pin textbox
        pin = request.form.get('userpin')

        rpi = database.query_rpi() # query rpi from db -Adrian

        #if no input is detected
        if rpi == None:
            return redirect(url_for('home.keypad'))
        else:
            #authenticate entered pin with the pin code in the db
            if rpi.pin_code == pin: #-Adrian
                #open door
                #led.on() 
                #sleep(10)
                #led.off()
                #TODO interface code between rpi and door lock
                return redirect(url_for('home.keypad'))
            else:
                return redirect(url_for('home.keypad'))
    else:
        return redirect(url_for('home.keypad'))

