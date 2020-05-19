import os

from flask import Blueprint
from app.controllers.home_controller import index_home
from app.controllers.measurements_controller import index_measurements, create_measurements, delete_measurements
from app.controllers.measurements_controller import generate_air_stations_map, show_map, generate_air_map
from app.controllers.magnitudes_controller import index_magnitudes, create_magnitudes, delete_magnitudes
from app.controllers.stations_controller import index_stations, create_stations, delete_stations
from app.controllers.days_controller import index_days, create_days, delete_days
from app.controllers.times_controller import index_times, create_times, delete_times
from app.controllers.sessions_controller import new_session

template_dir = os.path.abspath('app/views/')

app_blueprints = Blueprint('app', __name__, template_folder=template_dir)
app_blueprints.add_url_rule('/', view_func=index_home, methods=['GET'])

app_blueprints.add_url_rule('/measurements', view_func=index_measurements, methods=['GET'])
app_blueprints.add_url_rule('/measurements/create', view_func=create_measurements, methods=['POST'])
app_blueprints.add_url_rule('/measurements/delete', view_func=delete_measurements, methods=['POST'])
app_blueprints.add_url_rule('/measurements/generate_map', view_func=generate_air_stations_map, methods=['POST'])
app_blueprints.add_url_rule('/measurements/generate_air_map', view_func=generate_air_map, methods=['POST'])
app_blueprints.add_url_rule('/measurements/show', view_func=show_map, methods=['GET'])
app_blueprints.add_url_rule('/magnitudes', view_func=index_magnitudes, methods=['GET'])
app_blueprints.add_url_rule('/magnitudes/create', view_func=create_magnitudes, methods=['POST'])
app_blueprints.add_url_rule('/magnitudes/delete', view_func=delete_magnitudes, methods=['POST'])
app_blueprints.add_url_rule('/stations', view_func=index_stations, methods=['GET'])
app_blueprints.add_url_rule('/stations/create', view_func=create_stations, methods=['POST'])
app_blueprints.add_url_rule('/stations/delete', view_func=delete_stations, methods=['POST'])
app_blueprints.add_url_rule('/days', view_func=index_days, methods=['GET'])
app_blueprints.add_url_rule('/days/create', view_func=create_days, methods=['POST'])
app_blueprints.add_url_rule('/days/delete', view_func=delete_days, methods=['POST'])
app_blueprints.add_url_rule('/times', view_func=index_times, methods=['GET'])
app_blueprints.add_url_rule('/times/create', view_func=create_times, methods=['POST'])
app_blueprints.add_url_rule('/times/delete', view_func=delete_times, methods=['POST'])
app_blueprints.add_url_rule('/login', view_func=new_session, methods=['GET'])
