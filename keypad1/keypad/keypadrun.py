import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.ext.automap import automap_base
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@localhost/smart_lock'
db = SQLAlchemy(app)
Base = automap_base()
Base.prepare(db.engine, reflect=True) ## Connection information for database in object form which will reflect the database table attributes.
user = Base.classes.user ## create the "user" table in database as a class
results = db.session.query(user).all()
order = db.session.query(user) 
print(order)
              
def openWeb():
    port = 4444
    url = "http://127.0.0.1:"+str(port)
    print("~~~~~~~~~~~~~~~~~~~~~~~Openning~~~~~~~~~~~~~~~~~")
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()

@app.route('/', methods=['GET', 'POST'])
def index():
    for r in results:
        pinc = r.Pin_Code
        
        if request.method == 'POST':
            pin=request.form['code']

            if pinc == pin:
                print("adsd")
    return render_template('keypadhtml.html')
    


if __name__ == '__main__':
    openWeb()
    app.run(debug = True, use_reloader=False, port=4444)

