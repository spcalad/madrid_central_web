import os

from flask import Blueprint
from app.controllers.home_controller import index_home
from app.controllers.measurements_controller import index_measurements
from app.controllers.magnitudes_controller import index_magnitudes
from app.controllers.stations_controller import index_stations
from app.controllers.dates_controller import index_dates, create_dates
from app.controllers.sessions_controller import new_session

template_dir = os.path.abspath('app/views/')

app_blueprints = Blueprint('app', __name__, template_folder=template_dir)
app_blueprints.add_url_rule('/', view_func=index_home, methods=['GET'])

app_blueprints.add_url_rule('/measurements', view_func=index_measurements, methods=['GET'])
app_blueprints.add_url_rule('/magnitudes', view_func=index_magnitudes, methods=['GET'])
app_blueprints.add_url_rule('/stations', view_func=index_stations, methods=['GET'])
app_blueprints.add_url_rule('/dates', view_func=index_dates, methods=['GET'])
app_blueprints.add_url_rule('/dates/create', view_func=create_dates, methods=['POST'])
app_blueprints.add_url_rule('/login', view_func=new_session, methods=['GET'])
