from flask import render_template, request, redirect
from app.models.time import Time
from app import db

#@dates_blueprints.route('/')
def index_times():
    times = Time.query
    return render_template('times/index.html', times=times)

def create_times():
    times = Time.create_interval(request.form.get('initialTime'), request.form.get('finalTime'))
    for time in times:
        new_time = Time(id=time, hour=time)
        db.session.add(new_time)
        db.session.commit()
    return redirect('/times')

def delete_times():
    times = Time.query
    for time in times:
         db.session.delete(time)
         db.session.commit()
    return redirect('/times')
