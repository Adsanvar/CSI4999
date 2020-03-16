from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

##Creates db -Adrian
db = SQLAlchemy()
bcrypt = Bcrypt()

try:
    ##Creates the Flask Application with the configurations -Adrian
    def create_app():

        app = Flask(__name__)
        #allows us to use Login Manager and other tools suchas Flash from flask_login - Adrian
        app.config['SECRET_KEY'] = 'test_secret_key'
        #this configures the databse for communication with flask -jared
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:pass@localhost/smart_lock'
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
        # (return app) -Adrian
        db.init_app(app)

        bcrypt.init_app(app)
        
        #blueprints for the pages and models - Adrian
        from SmartLock.authenticator import auth as a_bp
        from SmartLock.web_server import home as h_bp

        app.register_blueprint(a_bp)
        app.register_blueprint(h_bp)

        return app

except:
    raise