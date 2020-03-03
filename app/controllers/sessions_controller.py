from flask import render_template

#@sessions_blueprints.route('/')
def new_session():
    return render_template('sessions/new.html')
