import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash, Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return 'Log In'

    