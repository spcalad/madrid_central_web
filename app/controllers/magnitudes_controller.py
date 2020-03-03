from flask import render_template

#@magnitudes_blueprints.route('/')
def index_magnitudes():
    return render_template('magnitudes/index.html')
