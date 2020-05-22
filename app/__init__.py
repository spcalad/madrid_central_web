import os

from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
login_manager = LoginManager()
db = SQLAlchemy()

def create_app():
    application = Flask(__name__, static_url_path='/static')
    application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    register_blueprints(application)
    initialize_extensions(application)
    return application

def register_blueprints(application):
    from app.controllers import app_blueprints
    application.register_blueprint(app_blueprints)

def initialize_extensions(application):
    from app.models.user import User
    db.init_app(application)
    login_manager.init_app(application)
    bootstrap.init_app(application)
