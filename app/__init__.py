import os
from flask import Flask, url_for, redirect

import Config
from Blueprints.User import user_bp
from Extensions import DATABASE, CACHE, LOGIN_MANAGER
from flask_migrate import Migrate

from Blueprints.Testing import test_bp

def create_app():
    #Setip Flask Config
    API_APP = Flask(__name__)
    API_APP.config.from_object(Config)
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    API_APP.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'Database', 'soccer.db')}"

    API_APP.secret_key = os.urandom(24)



    #Setup Flask Extensions
    migrate = Migrate(API_APP, DATABASE)
    DATABASE.init_app(API_APP)
    CACHE.init_app(API_APP)
    LOGIN_MANAGER.init_app(API_APP)






    #Add API ENDPOINTS HERE
    API_APP.register_blueprint(test_bp)
    API_APP.register_blueprint(user_bp)



    if __name__ == '__main__':
        API_APP.run(host='0.0.0.0', port=5002)

    return API_APP
