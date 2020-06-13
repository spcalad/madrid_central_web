from flask import render_template, request, redirect
from flask_paginate import Pagination, get_page_args
from app.models.station import Station
from app.models.station_duplicate import StationDuplicate
from app import db

#@stations_blueprints.route('/')
def index_stations():
    stations = Station.query.order_by(Station.category, Station.id)
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    per_page = 50
    pagination_stations = stations[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=stations.count(), css_framework='bootstrap4')
    return render_template('stations/index.html', stations=pagination_stations, page=page, per_page=per_page, pagination=pagination)

def create_stations():
    stations = Station.read_stations_file(request.files['file'], request.form.get('stationCategory'), request.form.get('monthFile'), request.form.get('yearFile'))

    for station in stations:
        new_station = Station(id=station[0], name=station[1], type=station[2],
                              address=station[3], latitude=station[4],
                              longitude=station[5], altitude=station[6],
                              start_date=station[7], category=station[8])

        Station.create(new_station)

    return redirect('/stations')

def delete_stations():
    db.session.query(Station).delete()
    db.session.query(StationDuplicate).delete()
    db.session.commit()
    return redirect('/stations')
