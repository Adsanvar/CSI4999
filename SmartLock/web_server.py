from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for
#from authenticator import auth
from flask_login import login_user, logout_user, login_required, current_user
from . import db, bcrypt
import SmartLock.database as database
#from gpiozero import LED
#from time import sleep

home = Blueprint('home', __name__)

#This Route is the index page (landing page) -Adrian
@home.route('/', methods=['GET'])
def index(): 
    return render_template('index.html')
   
@home.route('/', methods=['GET'])
def index_changed_password():
    flash('Password Successfully Changed', 'success')
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

    if 'confirm' in request.form:
        #checks to see if any field is empty 
        if request.form.get('member_username') and request.form.get('member_password') and request.form.get('firstname') and request.form.get('lastname') and request.form.get('email'):
            #Non-empty
            uname = request.form.get('member_username')
            pas = request.form.get('member_password')
            name = request.form.get('firstname')
            last = request.form.get('lastname')
            mail = request.form.get('email')
            #obtaines user from database thru ORM
            usr = database.User(username=uname, password = pas, first_name=name, last_name=last, role='Member', email=mail)
            database.create_user(usr)
            flash('Your new member has been created')
            return redirect(url_for('home.dashboard'))
        else:
            #empty
            flash('You have an empty field')
            return redirect(url_for('auth.dashboard'))
    #if confirm button is activated proceed with change of password

    if 'confirm1' in request.form: #if confirm button is clicked the dashboard
        #TODO: Query old RPI, by user_id. Then compare the pin codes
        #obtain input
        if request.form.get('old_rpi_pin'):

            old_pin = request.form.get('old_rpi_pin')
            rpi = database.query_rpi_by_id(current_user.id)
            new_pin = request.form.get('rpi_pin')
            confrim_pin = request.form.get('rpi_confirm_pin')

            if old_pin != new_pin:
                if old_pin == rpi.pin_code : 
                    #make sure they match, redirect to rpi_config with pas as a parameter - Adrian
                    if new_pin == confrim_pin:
                        flash('PIN SUCESSFULLY CHANGED', 'success')
                        return redirect(url_for('auth.rpi_config', sn=rpi.serial_number , pas=confrim_pin))
                    else:
                        flash('Oops, Looks like your confirmation PIN doesn\'t match', 'error')
                        return redirect(url_for('home.dashboard'))
                else: #if failed redirect to dashboard
                    flash('Oops, Looks like you mistyped your old PIN', 'error')
                    return redirect(url_for('home.dashboard'))
            else:#if failed redirect to dashboard
                    flash('You Cannot Have The Same PIN', 'error')
                    return redirect(url_for('home.dashboard'))
        else:
            flash('Enter A PIN', 'error')
            return redirect(url_for('home.dashboard'))

    #if confirm button is activated proceed with change of password
    if 'confirm2' in request.form:
        old_pass = request.form.get('old_password')
        new_pass = request.form.get('new_password')
        confrim_pass = request.form.get('confirm_password')
        print(old_pass, new_pass,confrim_pass)
        userpass = database.user_query(current_user.username)
        original_pass = userpass.password

        if bcrypt.check_password_hash(original_pass, old_pass):
            #checks to see if the inputed password is the same as the one in database
            if original_pass != new_pass: 
                #user can not change password to same password

                #make sure they match database, redirect to userpass with pas as a parameter - Brandon
                if new_pass == confrim_pass:
                    print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('Password confirmed'))
                    #current_user returns username by data representation of model
                    return redirect(url_for('auth.userpass', usr=current_user, pas=confrim_pass))
                else:
                    print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('Confirmation Failed'))
                    return redirect(url_for('home.dashboard'))

            else:#if failed redirect to dashboard
                flash('Password will not be changed')
                return redirect(url_for('home.dashboard'))
        else:#empty  
            print("errroooooooor")
            return redirect(url_for('home.dashboard'))

  

# #This route is the keypad page - Adrian
# @home.route("/keypad")
# @login_required
# def keypad():
#     #TODO: Update to the proper keypad.html file
#     return render_template('pinpad_test.html') 

# #This route is the keypad landing page for post commands
# @home.route("/keypad", methods=['POST'])
# @login_required
# def post_keypad():
#     #Jared
#     #if keypad enter button is pressed
#     if 'submitpin' in request.form:
#         #TODO error detection for keypad inputs to be entered here
#         print('IN SUBMIT')
#         #scrape input from the pin textbox
#         pin = request.form.get('userpin')

#         rpi = database.query_rpi() # query rpi from db -Adrian

#         #if no input is detected
#         if rpi == None:
#             return redirect(url_for('home.keypad'))
#         else:
#             #authenticate entered pin with the pin code in the db
#             if rpi.pin_code == pin: #-Adrian
#                 #open door
#                 #led.on() 
#                 #sleep(10)
#                 #led.off()
#                 #TODO interface code between rpi and door lock
#                 return redirect(url_for('home.keypad'))
#             else:
#                 return redirect(url_for('home.keypad'))
#     else:
#         return redirect(url_for('home.keypad'))

