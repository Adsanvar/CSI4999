from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for
#from authenticator import auth
from flask_login import login_user, logout_user, login_required, current_user
from . import db
import SmartLock.database as database
#from gpiozero import LED
#from time import sleep
#test led on RPI - Adrian
#led = LED(17) 

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
    if 'confirm2' in request.form: #if confirm button is clicked the dashboard
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
    # if 'confirm1' in request.form:
    #     #checks to see if any field is empty 
    #     if request.form.get('member_username') and request.form.get('member_password') and request.form.get('firstname') and request.form.get('lastname') and request.form.get('email'):
    #         #Non-empty
    #         uname = request.form.get('member_username')
    #         pas = request.form.get('member_password')
    #         name = request.form.get('firstname')
    #         last = request.form.get('lastname')
    #         mail = request.form.get('email')
    #         #obtaines user from database thru ORM
    #         usr = database.User(username=uname, password = pas, first_name=name, last_name=last, role='Member', email=mail)
    #         database.create_user(usr)
    #         flash('Your new member has been created')
    #         return redirect(url_for('home.dashboard'))
    #     else:
    #         #empty
    #         flash('You have an empty field')
    #         return redirect(url_for('home.dashboard'))
    # #if confirm button is activated proceed with change of password
    # if 'confirm3' in request.form:
    #     old_pass = request.form.get('old_password')

    #     userpass = database.query_user()
    #     if request.form.get('original_password') and request.form.get('new_password') and request.form.get('confirm_password'):
    #         #checks to see if a field is empty
    #         if request.form.get('original_password') != request.form.get('new_password'): 
    #             #user can not change password to same password
    #             if old_pass == userpass.password : 
    #                 #make sure they match database, redirect to userpass with pas as a parameter - Brandon
    #                 new_pass = request.form.get('new_password')
    #                 confrim_pass = request.form.get('confirm_password')
    #                 if new_pass == confrim_pass:
    #                     print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('Password confirmed'))
    #                     return redirect(url_for('auth.userpass', pas=confrim_pass))
    #                 else:
    #                     print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('Confirmation Failed'))
    #                     return redirect(url_for('home.dashboard'))
    #             else: #if failed redirect to dashboard
    #                 print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('Password was not confirmed'))
    #                 return redirect(url_for('home.dashboard'))
    #         else:#if failed redirect to dashboard
    #             flash('Password will not be changed')
    #             return redirect(url_for('home.dashboard'))
    #     else:#empty  
    #         flash('Every input is required')
    #         return redirect(url_for('home.dashboard'))


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

