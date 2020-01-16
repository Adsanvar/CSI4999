import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash

#Creates the application module to run upon running script -Adrian
app = Flask(__name__)

#This Route is the index page (landing page)
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
   


@app.route('/singup', methods=['GET', 'POST'])
def signup():
    return 'Sign UP'


#Main function that executes the application
if __name__ == '__main__':
    #runs the flask application using an IP Address, Debug set to true so test the site and modify on the fly
    app.run(debug=True, host='192.168.1.65')

