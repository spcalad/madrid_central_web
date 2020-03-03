from flask import render_template

#@stations_blueprints.route('/')
def index_stations():
    return render_template('stations/index.html')
