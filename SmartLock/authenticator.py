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
        
@auth.route('/changePassword')
def changePassword():
    return render_template('changePassword.html')


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
        return render_template('signup.html',firstname = first, lastname = last, email = email, serialnum = serial , info = error)
    if mode == 'email_exists':
         return render_template('signup.html', info = error)
    if mode == 'email_failed':
        return render_template('signup.html', username = uname, firstname = first, lastname = last, serialnum = serial , info = error)
    if mode == 'invalid_smartlock':
        return render_template('signup.html', info = error)
    if mode == 'inactive_smartlock':
        return render_template('signup.html', info = error)

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
        #this array contains user's information
        lst = []
        lst.append(uname)
        lst.append(name)
        lst.append(last)
        lst.append(mail)
        lst.append(serial)

        #check to make sure the user is unique -Adrian
        if database.user_query(uname) == None:
            #checks to make sure that the email is valid
            if database.query_userByEmail(mail) == None:
                if validate_email(mail):

                    #Checks to make sure the RPI
                    # - Exists in our Database
                    # - Is Active
                    if database.query_rpi(serial) != None:

                        if database.query_rpi(serial).active == True:

                            #subject = 'Welcome To SmartLock, Please Vertify Your Email.'
                            msg = 'http://localhost:5000/verification/'+uname+'/'+serial
                            #msg = 'http://172.20.10.2:5000/verification/'+uname+'/'+serial
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
                            usr = database.User(username=uname, password = bcrypt.generate_password_hash(pas).decode('utf-8'), first_name=name, last_name=last, role='Member', email=mail, verified = False)
                            database.create_user(usr)
                            return redirect(url_for('auth.vertification_post'))
                        else:
                            lst.append('Smart Lock Is Not Active. Please Activate The Smart Lock.')
                            lst.append('inactive_smartlock')
                            data = ','.join(lst)
                            return redirect(url_for('auth.signupUserError', data = data))
                    else:
                        lst.append('Smart Lock Does Not Exist.')
                        lst.append('invalid_smartlock')
                        data = ','.join(lst)
                        return redirect(url_for('auth.signupUserError', data = data))
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
@auth.route('/verification/<key>/<serial>', methods=['GET'])
def verification_return(key, serial):
    if database.user_query(key) == None:
        return redirect(url_for('auth.login_index'))
    else: 
        usr = database.user_query(key)
        database.verify_user(usr)
        database.rpi_user(serial ,usr.id)
        return redirect(url_for('auth.login_index'))

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
    database.activate_pi(sn, True)
    return "Success"

#Route to get pin_code
@auth.route('/getPin/<username>/<password>/<sn>', methods=['GET'])
def getPiInformation(username,password,sn):
    rpi = database.query_rpi(sn)
    user = database.user_query(username)
    if rpi.serial_number == None or rpi.active == False:
        return abort(400)
    elif rpi.serial_number != None and rpi.active != False:
        #if initial check of sn and status is successful,
        # check for verification in the rpi db -jared
        if user.verified == 0:
            return abort(400)
        elif user.verified == 1:
            return rpi.pin_code

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

@auth.route('/piLogin/<username>/<password>', methods=['GET'])
def piLogin(username, password):
    #obtaines user from database thru ORM
    usr = database.user_query(username)
    #checks if usr returned is null if so redirect to the login
    if usr == None:
        return abort(400)
    else:
        if usr.username == username and bcrypt.check_password_hash(usr.password, password) and usr.verified == True: 
            #login_user(usr) #if usr is rpi redirect them to the keypad route in web_server.py
            return 'Success'
            
        else: 
            return abort(400)


# Mobile Login API Call - Adrian
# Query Database for user, Check if object in db, logic for login
@auth.route('/mobilelogin/<username>/<password>', methods=['GET'])
def mobilelogin(username,password):
    usr = database.user_query(username)
    if usr == None:
        return 'Failed', 400
    else:
        if usr.username == username and bcrypt.check_password_hash(usr.password, password) and database.user_query(username).verified == True: 
            return 'Success', 200
        else:
            return 'Failed', 400

