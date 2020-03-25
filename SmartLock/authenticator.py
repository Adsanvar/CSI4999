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
    return render_template('keypad.html')

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
            conn = http.client.HTTPConnection("adsanvar.pythonanywhere.com")
            #conn.request("GET", '/getPiInfo/'+getserial())
            conn.request("GET", '/piLogin/'+name +'/'+pas)

            r1 = conn.getresponse()
            res = r1.read().decode('utf8')
            print(res)

            if res == 'Success':
                #conn2 = http.client.HTTPConnection("http://adsanvar.pythonanywhere.com",5000)
                conn2 = http.client.HTTPConnection("adsanvar.pythonanywhere.com")
                serial = getserial()
                conn2.request("GET", '/getPin/'+name +'/'+pas+'/'+getserial())

                r2 = conn2.getresponse()
                result = r2.read().decode('utf8')
                #hashing doesn't not work in MariaDB
                #bcrypt.generate_password_hash(result).decode('utf-8')
                pi = database.query_rpi()
                database.update_pi(pi, result)

                return redirect(url_for('auth.keypad'))
            else:
                return render_template('index.html', info = 'Invalid Credentials')

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
    pin=request.form['code']
    rpi = database.query_rpi()
    if rpi.pin_code == pin:
        GPIOon()
    return redirect(url_for('auth.keypad'))

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
