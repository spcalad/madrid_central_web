from flask_bootstrap import Bootstrap
from flask import Flask

bootstrap = Bootstrap()

def create_app():
    application = Flask(__name__)
    register_blueprints(application)
    bootstrap.init_app(application)
    return application

def register_blueprints(application):
    from app.controllers import app_blueprints
    application.register_blueprint(app_blueprints)
