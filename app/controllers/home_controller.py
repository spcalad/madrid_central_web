from flask import render_template

#@home_blueprints.route('/')
def index_home():
    return render_template('home/index.html')
