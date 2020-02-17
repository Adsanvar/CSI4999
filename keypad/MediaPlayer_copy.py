import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash
app = Flask(__name__)

def openWeb():
    port = 8080
    url = "http://127.0.0.1:"+str(port)
    print("~~~~~~~~~~~~~~~~~~~~~~~Openning~~~~~~~~~~~~~~~~~")
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('keypadhtml.html')

if __name__ == '__main__':
    openWeb()
    app.run(debug = True, use_reloader=False, port=8080)

