from flask import render_template

#@measurements_blueprints.route('/')
def index_measurements():
    return render_template('measurements/index.html')
