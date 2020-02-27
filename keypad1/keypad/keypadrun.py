import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123eid123@localhost/smart_lock'


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True)
    pincode = db.Column('pincode', db.String(45))
def openWeb():
    port = 4444
    url = "http://127.0.0.1:"+str(port)
    print("~~~~~~~~~~~~~~~~~~~~~~~Openning~~~~~~~~~~~~~~~~~")
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pin=request.form['code']
        print(pin)
        examples = User.query.all()
        #for ex in examples:
            #print(ex.data)
        


    return render_template('keypadhtml.html')


if __name__ == '__main__':
    openWeb()
    app.run(debug = True, use_reloader=False, port=4444)

