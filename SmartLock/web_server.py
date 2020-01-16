import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash
from authenticator import auth
#Creates the application module to run upon running script -Adrian
app = Flask(__name__)
app.register_blueprint(auth)

#This Route is the index page (landing page)
@app.route('/', methods=['GET'])
def index(): 
    return render_template('index.html')
   


#Main function that executes the application
if __name__ == '__main__':
    #runs the flask application using an IP Address, Debug set to true so test the site and modify on the fly
    app.run(debug=True)

