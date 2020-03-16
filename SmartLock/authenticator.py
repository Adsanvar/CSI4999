import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash, Blueprint, redirect, url_for
from flask_login import login_user, logout_user, login_required
from . import db, bcrypt
import SmartLock.database as database
from SmartLock.controller import GPIOon, GPIOoff
import http.client
import numpy as np

#sets up the authenticator blueprint - Adrian
auth = Blueprint('auth', __name__)

#Standard login function that loads the index.html - Adrian
@auth.route('/', methods=['GET'])
def index():
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
            #Send http request
            #http://192.168.1.65:5000/
            conn = http.client.HTTPConnection("192.168.1.65",5000)
            #conn.request("GET", '/getPiInfo/'+getserial())
            conn.request("GET", '/piLogin/'+name +'/'+pas)

            r1 = conn.getresponse()
            print(r1.read())
            if 'Bad Request' in r1.read().decode('utf8'):
                return redirect(url_for('auth.index', info = 'Invalid Credentials'))
            elif 'Success' == r1.read().decode('utf8'):
                conn.request("GET", '/getPin/'+name +'/'+pas+'/'+"124")

                r2 = conn.getresponse()
                print(r2.read().decode('utf8'))
                return redirect(url_for('auth.keypad'))
            else:
                return redirect(url_for('auth.index', info='Error'))

            # if context.h1.string != 'Bad Request':
            #     print(r1.read().decode('utf8'))
            #     return redirect(url_for('auth.keypad'))
            # else:
            #     return redirect(url_for('auth.login'))

            # #checks if usr returned is null if so redirect to the login
            # if r1.read() == None:
            #     return redirect(url_for('auth.login'))
            # else:
            #     #authenticates user to db
            #     if usr.username == name and usr.password == pas:
            #         #Determines the role of the logged in user - Adrina
            #         if usr.role == 'rpi':
            #             login_user(usr) #if usr is rpi redirect them to the keypad route in web_server.py
            #             return redirect(url_for('home.keypad'))
            #     else:
            #         return redirect(url_for('auth.login'))
        else:
            #empty
            return redirect(url_for('auth.index'))
            

#Route for changing RPI Password
@auth.route('/rpi/<pas>')
def rpi_config(pas):
    rpi = database.query_rpi()
    database.update_pi(rpi, pas)

    return redirect(url_for('home.dashboard'))


#This route is the keypad landing page for post commands
@auth.route("/keypad", methods=['GET'])
def keypad():
    return render_template('keypad.html')

#This route is the keypad landing page for post commands
@auth.route("/keypad", methods=['POST'])
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
                GPIOon()
                #TODO interface code between rpi and door lock
                return redirect(url_for('home.keypad'))
            else:
                return redirect(url_for('home.keypad'))
    else:
        return redirect(url_for('home.keypad'))

def getserial():
    serialNum = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                serialNum = line[10:26]
        f.close()
    except:
        raise
    return serialNum

