from flask import Flask, render_template, request, flash, Blueprint, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required
from . import db, bcrypt
import SmartLock.database as database
from validate_email import validate_email
from email.mime.text import MIMEText
import os

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
                # Checks db.password hash with form password - Heath
                # Also checks if the user is verified before logging in - Heath
                #if usr.username == name and usr.password == pas and database.user_query(name).verified == True: 
                if usr.username == name and bcrypt.check_password_hash(usr.password, pas) and database.user_query(name).verified == True: 
                #if usr.username == name and usr.password == pas:
                    #Determines the role of the logged in user - Adrina
                    if usr.role == 'Member':
                        #route to dashboard and update the login session
                        login_user(usr)
                        return redirect(url_for('home.dashboard'))
                else:
                    return redirect(url_for('auth.login'))
        else:
            #empty
            return redirect(url_for('auth.login'))
            
    #if signup button clicked send to signup page        
    if 'signup' in request.form:
        return redirect(url_for('auth.signup'))
       
    if 'forgot' in request.form:
        return redirect(url_for('auth.changePassword'))                           
        
#route for the signup - Adrian
@auth.route('/signup')
def signup_index():
    return render_template('signup.html')

#Route to specify what caused the error and load appropiate fields
@auth.route('/signupUserError/<data>', methods = ['GET'])
def signupUserError(data):
    w = data.split(',')
    uname = w[0]
    first = w[1]
    last = w[2]
    email = w[3]
    serial = w[4]
    error = w[5]
    mode = w[6]
    #this mode is used to distinguish what to display on screen
    if mode == 'user':
        return render_template('signup.html',firstname = first, lastname = last, email = email, info = error)
    if mode == 'email_exists':
         return render_template('signup.html', info = error)
    if mode == 'email_failed':
        return render_template('signup.html', username = uname, firstname = first, lastname = last, info = error)
    if mode == 'invalid_smartlock':
        return render_template('signup.html', info = error)
    if mode == 'inactive_smartlock':
        return render_template('signup.html', info = error)

#route for the sign up post command - Adrian
@auth.route('/signup', methods=['POST'])
def signup():
    #Authentication Code Goes Here - Adrian

    #checks to see if the the username field is empty -Adrian
    if request.form.get('signup_username') and request.form.get('signup_password') and request.form.get('firstname') and request.form.get('lastname') and request.form.get('email'):
        #Non-empty
        uname = request.form.get('signup_username')
        pas = request.form.get('signup_password')
        name = request.form.get('firstname')
        last = request.form.get('lastname')
        mail = request.form.get('email')
        #this array contains user's information
        lst = []
        lst.append(uname)
        lst.append(name)
        lst.append(last)
        lst.append(mail)

        #check to make sure the user is unique -Adrian
        if database.user_query(uname) == None:
            #checks to make sure that the email is valid
            if database.query_userByEmail(mail) == None:
                if validate_email(mail):
                    #subject = 'Welcome To SmartLock, Please Vertify Your Email.'
                    #msg = 'http://localhost:5000/verification/'+uname+'/'+serial
                    msg = 'http://adsanvar.pythonanywhere.com/verification/'+uname
                    #msg = 'http://172.20.10.2:5000/verification/'+uname+'/'+serial
                    sendMail(mail, msg)
                    # msg = 'http://localhost:5000/verification/james'
                    # sendMail('ertech404@gmail.com', msg)
                    # return redirect(url_for('auth.vertification_post'))
                    # return redirect(url_for('auth.vertification_post'))
                    # if sendMail(mail, msg)
                        #print(mail, "\t", msg)
                    # created hashed password - Heath
                    usr = database.User(username=uname, password = bcrypt.generate_password_hash(pas).decode('utf-8'), first_name=name, last_name=last, role='Member', email=mail, verified = False, sensitivity=0)
                    #usr = database.User(username=uname, password = pas, first_name=name, last_name=last, role='Member', email=mail, verified = False)

                    database.create_user(usr)
                    return redirect(url_for('auth.vertification_post'))


                else:
                    lst.append('Email Syntax Invalid. Please Re-enter Email.')
                    lst.append('email_failed')
                    data = ','.join(lst)
                    return redirect(url_for('auth.signupUserError', data = data))
            else:
                lst.append('This Email Appears To Be Taken. If You Forgot Your Password Please Reset.')
                lst.append('email_exists')
                data = ','.join(lst)
                return redirect(url_for('auth.signupUserError', data = data))
        else:
            #Adds datum to route for user friend field updates 
            lst.append('Username is already taken. Please Choose Another Username.')
            lst.append('user')
            data = ','.join(lst)
            return redirect(url_for('auth.signupUserError', data = data))
    else:
        #empty
        return redirect(url_for('auth.signup'))

#Route to handle vertification screen
@auth.route('/vertification', methods=['POST','GET'])
def vertification_post():
    if request.method == 'POST':
        if request.form.get('vertification_login'):
            return redirect(url_for('auth.login_index'))
    else:
        return render_template('vertification.html')

#Route for verifying
@auth.route('/verification/<key>', methods=['GET'])
def verification_return(key):
    if database.user_query(key) == None:
        return redirect(url_for('auth.login_index'))
    else: 
        usr = database.user_query(key)
        database.verify_user(usr)
        return redirect(url_for('auth.login_index'))

#Route for changing RPI Password
@auth.route('/rpi/<sn>/<pas>')
@login_required
def rpi_config(sn, pas):
    print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('INIDE RPI'))
    database.update_pi(sn, pas)
    print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('SUCCESS'))
    return redirect(url_for('home.dashboard'))

#Route for changing User Password
@auth.route('/userpass/<usr>/<pas>')
@login_required
def userpass(usr, pas):
    print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('INIDE User'))
    database.update_pass(usr, bcrypt.generate_password_hash(pas).decode('utf-8'))
    return redirect(url_for('home.dashboard'))

# lines 188-275 are the forgot password, in detail the changePassword.html is the place where the user enters his
# email. forgotpass.html is the place where user enters the confirm password. 
@auth.route('/changePassword')
def changePassword_index():
    return render_template('changePassword.html')
# much like the signup page this emails the user
@auth.route('/changePassword', methods=['POST'])
def changePassword():
    if 'confirm' in request.form:
        if request.form.get('email'):
            #Non-empty
            mail = request.form.get('email')
            #this array contains user's information
            lst = []
            lst.append(mail)
            usr = database.query_userByEmail(mail)
            #checks to make sure that the email is valid
            if usr != None:
                if validate_email(mail):
                    uname = usr.username
                    #subject = 'Welcome To SmartLock, Please Vertify Your Email.'
                    msg = 'http://localhost:5000/forgotpass/'+uname
                    #msg = 'http://172.20.10.2:5000/forgotpass/'+uname
                    print(msg)
                    print(mail)
                    sendMail(mail, msg)
                        # msg = 'http://localhost:5000/verification/james'
                        # sendMail('ertech404@gmail.com', msg)
                        # return redirect(url_for('auth.vertification_post'))
                        # return redirect(url_for('auth.vertification_post'))
                        # if sendMail(mail, msg):
                        #print(mail, "\t", msg)
                            # created hashed password - Heath
                        # usr = database.User(username=uname, email=mail)
                        #  database.create_user(usr)
                    return redirect(url_for('auth.forgotpass_post'))
                ##### ONCE creating forgotpassError underneath this will need to be implemented
                else:
                    #    lst.append('Email Syntax Invalid. Please Re-enter Email.')
                    #    lst.append('email_failed')
                    #    data = ','.join(lst)
                    return redirect(url_for('auth.signupUserError', data = data))
            
            else:
                return redirect(url_for('auth.signupUserError', data = data))
        else:
            #empty
            return redirect(url_for('auth.changePassword'))
#like verification this the route handling the the screen
@auth.route('/forgotpass', methods=['POST','GET'])
def forgotpass_post():
    if request.method == 'POST':
        if request.form.get('confirm'):
            return redirect(url_for('auth.login_index'))
    else:
        return render_template('forgotpass.html')
# this the route handling the input of the passwords 
@auth.route('/forgotpass/<uname>', methods=['GET'])
def forgotpass_return(uname):
    if database.user_query(uname) == None:
        return redirect(url_for('auth.signup_index'))
    else: 
        usr = database.user_query(uname)
        new_pass = request.form.get('password')
        confrim_pass = request.form.get('confirm_password')
        print( new_pass,confrim_pass)
        original_pass = usr.password
            #user can not change password to same password
            if original_pass != new_pass: 
                #make sure they match database, redirect to userpass with pas as a parameter - Brandon
                if new_pass == confrim_pass:
                    print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('Password confirmed'))
                    #current_user returns username by data representation of model
                    return redirect(url_for('auth.changepass', usr=uname, pas=confrim_pass))
                else:
                    print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('Confirmation Failed'))
                    return redirect(url_for('auth.forgotpass'))

            else:#if failed redirect to dashboard
                flash('Password will not be changed')
                return redirect(url_for('auth.forgotpass'))

        return redirect(url_for('auth.login_index'))
#Route for changing forgotten password
@auth.route('/changepass/<usr>/<pas>')
def changepass(usr, pas):
    print('@@@@@@@@@@@@@@@@@@@@@@@@ {}'.format('INIDE User'))
    database.update_pass(usr, bcrypt.generate_password_hash(pas).decode('utf-8'))
    return redirect(url_for('auth.login_index'))

#route to logout the user from the session - Adrian 
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))

#Route to set active status -jared (referenced from Adrian)
@auth.route('/setActive/<sn>/<ip>', methods=['GET'])
def setActive(sn, ip):
    database.activate_pi(sn, True)
    database.setIp(sn, ip)
    return "Success"

#Route to get pin_code
@auth.route('/getPin/<username>/<password>/<sn>', methods=['GET'])
def getPiInformation(username,password,sn):
    rpi = database.query_rpi(sn)
    user = database.user_query(username)
    if rpi.serial_number == None or rpi.active == False:
        return abort(400)
    elif rpi.serial_number != None and rpi.active:
        #if initial check of sn and status is successful,
        # check for verification in the rpi db -jared
        if user.verified:
            return rpi.pin_code
        else:
            return abort(400)
            

#check if the serial number is active or not
def checkActive(serial_number):
    try:
        #query rpi table
        
        return True 
    except:
        return False

 #sends mail to the intended user
# def sendMail(to, message):
#     try:
#         s = smtplib.SMTP('smtp.gmail.com', 587)

#         # s.starttls()
#         # s.login("smartlock.vertification.noreply@gmail.com", "TESt123!")
        
#         # s.sendmail("smartlock.vertification.noreply@gmail.com", "ertech404@gmail.com", message)
#         # s.quit()
#         s.starttls()
#         s.login("pitest873@gmail.com", "TESt123!")

#         s.sendmail("pitest873@gmail.com", "ertech404@gmail.com", message)
#         s.quit()
#         return True
#     except:
#         raise
#         return False

# def sendMail(to, message):
#     os.system("python sendmail.py {} {}".format(to, message))

def sendMail(to, message):
    import smtplib, sys

    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()
        s.login("smartlock.vertification.noreply@gmail.com", "TESt123!")
                
        #s.sendmail("pitest873@gmail.com", sys.argv[1], sys.argv[2])
        #msg = 'http://localhost:5000/verification/adrian/'
        msg = "WELCOME TO SMART LOCK\n" + message
        s.sendmail("smartlock.vertification.noreply@gmail.com", to, msg)
        s.quit()
    except:
        raise

@auth.route('/piLogin/<username>/<password>/<serial>', methods=['GET'])
def piLogin(username, password, serial):
    #obtaines user from database thru ORM
    usr = database.user_query(username)
    #checks if usr returned is null if so redirect to the login
    if usr == None:
        return abort(400)
    else:
        if usr.username == username and bcrypt.check_password_hash(usr.password, password) and usr.verified == True: 
            #login_user(usr) #if usr is rpi redirect them to the keypad route in web_server.py
            rpi = database.query_rpi(serial)
            rpi.user_id = usr.id
            return 'Success'
            
        else: 
            return abort(400)


# Mobile Login API Call - Adrian
# Query Database for user, Check if object in db, logic for login
@auth.route('/mobilelogin/<username>/<password>', methods=['GET'])
def mobilelogin(username, password):
    usr = database.user_query(username)
    if usr == None:
        return 'Failed', 400
    else:
        if usr.username == username and bcrypt.check_password_hash(usr.password, password) and database.user_query(username).verified == True: 
            return 'Success', 200
        else:
            return 'Failed', 400

#Gets pin code and ip address of the user's rpi when called (used for mobile) -Adrian
@auth.route('/getUserInfo/<usr>', methods=['GET'])
def getUserInfo(usr):
    data = database.get_mobile_information(usr)
    return data

@auth.route('/setSensitivity/<usr>/<sen>', methods=['GET'])
def setSensitivity(usr, sen):
    database.setSensitivity(usr,sen)
    return 'Success'
