from flask import render_template, request, redirect
from app.models.station import Station
from app import db

#@stations_blueprints.route('/')
def index_stations():
    stations = Station.query
    return render_template('stations/index.html', stations=stations)

def create_stations():
    stations = Station.read_stations_file(request.files['file'])
    for station in stations:
        new_station = Station(id=station[0], name=station[1], type=station[2],
                              address=station[3], latitude=station[4],
                              longitude=station[5], altitude=station[6],
                              start_date=station[7])
        db.session.add(new_station)
        db.session.commit()
    return redirect('/stations')

def delete_stations():
    stations = Station.query
    for station in stations:
         db.session.delete(station)
         db.session.commit()
    return redirect('/stations')
