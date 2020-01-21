from flask import Flask
from flask_sqlalchemy import SQLAlchemy

##Creates db -Adrian
db = SQLAlchemy()

##Creates the Flask Application with the configurations
def create_app():

    app = Flask(__name__)

    #this configures the databse for communication with flask -jared
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Database13.@localhost/smart_lock'

    db.init_app(app)

    from SmartLock.authenticator import auth as a_bp

    app.register_blueprint(a_bp)

    from SmartLock.web_server import home as h_bp

    app.register_blueprint(h_bp)

    return app
