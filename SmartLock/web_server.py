import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash
from authenticator import auth
#Creates the application module to run upon running script -Adrian
app = Flask(__name__)
app.register_blueprint(auth) #registers the authenticator auth routing to this module - Adrian

#This Route is the index page (landing page) -Adrian
@app.route('/', methods=['GET'])
def index(): 
    return render_template('index.html')
   

#Main function that executes the application -Adrian
if __name__ == '__main__':
    #runs the flask application using an IP Address, Debug set to true so test the site and modify on the fly
    app.run(debug=True)

