import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash, Blueprint

#sets up the authenticator blueprint
auth = Blueprint('auth', __name__)

#route for the login 
@auth.route('/login', methods=['GET', 'POST'])
def login():
    return 'Log In'

    