import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash, Blueprint, session, redirect, url_for
#from authenticator import auth
from flask_login import login_user, logout_user, login_required, current_user
from . import db
import SmartLock.database as database
from gpiozero import LED
from time import sleep
from SmartLock.controller import GPIOon, GPIOoff


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
    if 'confirm' in request.form: #if confirm button is clicked the dashboard
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

