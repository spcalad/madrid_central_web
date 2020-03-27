import os

from flask import Blueprint
from app.controllers.home_controller import index_home
from app.controllers.measurements_controller import index_measurements
from app.controllers.magnitudes_controller import index_magnitudes, create_magnitude, delete_magnitudes
from app.controllers.stations_controller import index_stations, create_stations, delete_stations
from app.controllers.dates_controller import index_dates, create_dates, delete_dates
from app.controllers.sessions_controller import new_session

template_dir = os.path.abspath('app/views/')

app_blueprints = Blueprint('app', __name__, template_folder=template_dir)
app_blueprints.add_url_rule('/', view_func=index_home, methods=['GET'])

app_blueprints.add_url_rule('/measurements', view_func=index_measurements, methods=['GET'])
app_blueprints.add_url_rule('/magnitudes', view_func=index_magnitudes, methods=['GET'])
app_blueprints.add_url_rule('/magnitudes/create', view_func=create_magnitude, methods=['POST'])
app_blueprints.add_url_rule('/magnitudes/delete', view_func=delete_magnitudes, methods=['POST'])
app_blueprints.add_url_rule('/stations', view_func=index_stations, methods=['GET'])
app_blueprints.add_url_rule('/stations/create', view_func=create_stations, methods=['POST'])
app_blueprints.add_url_rule('/stations/delete', view_func=delete_stations, methods=['POST'])
app_blueprints.add_url_rule('/dates', view_func=index_dates, methods=['GET'])
app_blueprints.add_url_rule('/dates/create', view_func=create_dates, methods=['POST'])
app_blueprints.add_url_rule('/dates/delete', view_func=delete_dates, methods=['POST'])
app_blueprints.add_url_rule('/login', view_func=new_session, methods=['GET'])
