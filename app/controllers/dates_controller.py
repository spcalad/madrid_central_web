from flask import render_template

#@dates_blueprints.route('/')
def index_dates():
    return render_template('dates/index.html')
