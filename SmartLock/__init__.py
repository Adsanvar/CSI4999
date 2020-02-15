from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager as manager

##Creates db -Adrian
db = SQLAlchemy()

##Creates the Flask Application with the configurations -Adrian
def create_app():

    app = Flask(__name__)
    #allows us to use Login Manager and other tools suchas Flash from flask_login - Adrian
    app.config['SECRET_KEY'] = 'test_secret_key'
    #this configures the databse for communication with flask -jared
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://adsanvar:Database13.@adsanvar.mysql.pythonanywhere-services.com/smart_lock'

    # (return app) -Adrian
    db.init_app(app)
    db.creatall()

    #initialized the login manager - Adrian
    LoginManager = manager()
    LoginManager.login_view = 'auth.login'
    LoginManager.init_app(app)

    #blueprints for the pages and models - Adrian
    from SmartLock.authenticator import auth as a_bp
    from SmartLock.web_server import home as h_bp

    app.register_blueprint(a_bp)
    app.register_blueprint(h_bp)

    #used to query load the logged in user
    from SmartLock.database import user_id_query as id_query

    @LoginManager.user_loader
    def load_user(id):
        return id_query(id)

    return app