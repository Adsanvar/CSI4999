import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash
from authenticator import auth
from flask_login import login_user, logout_user, login_required

#Creates the application module to run upon running script -Adrian
app = Flask(__name__)
app.register_blueprint(auth) #registers the authenticator auth routing to this module - Adrian

#This Route is the index page (landing page) -Adrian
@app.route('/', methods=['GET'])
def index(): 
    return render_template('index.html')
   
#This routes is the dashboard page -Adrian
@app.route('/dashboard')
@login_required
def dashboard():
    return 'Dashboard' 

#Main function that executes the application -Adrian
if __name__ == '__main__':
    #runs the flask application using an IP Address, Debug set to true so test the site and modify on the fly
    app.run(debug=True)

