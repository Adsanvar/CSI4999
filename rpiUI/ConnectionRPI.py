import http.client
import os, threading, webbrowser, subprocess
from flask_login import LoginManager
from flask import Flask, render_template, flash, request, url_for, redirect

app = Flask(__name__)
def openWeb():
    port = 8080
    url = "http://127.0.0.1:"+str(port)
    print("~~~~~~~~~~~~~~~~~~~~~~~Openning~~~~~~~~~~~~~~~~~")
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()


@app.route('/', methods=["GET","POST"])
def login_page():
    
    if request.method == "POST":
        print("test")
        username = request.form['user']
        password = request.form['pass']
        if username or password == None:
            print("error")
            
        else: 
            print(username)
            print("sdfsdfsdfsdfsdf")
            conn = http.client.HTTPConnection("localhost",5000)
            conn.request("GET", '/piLogin/'+ 'testing/'+'test/'+'123')
            r1 = conn.getresponse()
            pin = r1.read().decode('utf-8')
            print(pin)
        #flash(username)
        #flash(password)
        #print(username)
        #print("asdasd")
        #connect(username,password)
    #print("sdasdasdasd")
    return render_template("rpiUI.html",error=error)
    
    
    
    
# def connect():
#     if usern == None:
#         return render_template("rpiUI.html")
#     else:
#login_page()
# print("!23123123123123123")
# def connect(username,password):
#     print(username)
#     conn = http.client.HTTPConnection("localhost",5000)
#     conn.request("GET", '/piLogin/'+ 'testing/'+'test/'+'123')
#     r1 = conn.getresponse()
#     pin = r1.read().decode('utf-8')
#     print(pin)
    
#login_page()
# conn = http.client.HTTPConnection("localhost",5000)
# conn.request("GET", '/piLogin/'+ 'testing/'+'test/'+ '123')
# r1 = conn.getresponse()
# pin = r1.read().decode('utf-8')
# print(pin)

if __name__ == '__main__':
    openWeb()
    app.run(debug = True, use_reloader=False, port=8080)