from flask import render_template
import pandas as pd
from flask import render_template, request, redirect
from app.models.measurement import Measurement, FileReader#, Plotter
from app.models.station import Station
from app.models.day import Day
from app import db


#@measurements_blueprints.route('/')
def index_measurements():
    measurements = db.session.query(Measurement).limit(20)
    return render_template('measurements/index.html', measurements=measurements)


def create_measurements():
    measurement_obj = FileReader()
    if measurement_obj.read_measurement_file(request.files['file']):
        measurements = []
        for measurement in measurement_obj.maintable:
            measurements.append(Measurement(
                station_id=measurement[0],
                day_id=measurement[1],
                time_id=measurement[2],
                magnitude_id=measurement[3],
                value=measurement[4],
                validation=measurement[5]
            ))

        db.session.add_all(measurements)
        db.session.commit()

    return redirect('/measurements')


def generate_air_stations_map():
    plotter = Plotter()
    station_data_query = db.session.query(Station.id,
                                          Station.name,
                                          Station.type,
                                          Station.latitude,
                                          Station.longitude).all()

    station_data_df = pd.DataFrame(station_data_query, columns=['id', 'name', 'type', 'latitude', 'longitude'])

    plotter.add_air_station_marker(locations=station_data_df.iloc[:, [3, 4]].values,
                                   station_names=station_data_df.iloc[:, [1]].values)
    plotter.generate_map()
    return redirect('/measurements/show')


def generate_air_map():
    date_input = request.form.get('initialDay')
    print(date_input)
    plotter = Plotter()
    query_data = db.session.query(Measurement.station_id,
                                  Station.latitude,
                                  Station.longitude,
                                  Station.name,
                                  Measurement.time_id,
                                  Day.day,
                                  Day.month,
                                  Day.year,
                                  Measurement.value,
                                  Measurement.magnitude_id).join(
        Station, Station.id == Measurement.station_id).join(
        Day, Measurement.day_id == Day.id).filter(
        Day.year == 2016, Day.month == 1,
        Measurement.station_id == 28079035,
        Measurement.magnitude_id == 8).order_by(Measurement.magnitude_id, Day.year, Day.month, Day.day,
                                                Measurement.time_id).all()

    air_data_df = pd.DataFrame(query_data, columns=['id',
                                                    'latitude',
                                                    'longitude',
                                                    'name',
                                                    'time',
                                                    'day',
                                                    'month',
                                                    'year',
                                                    'value',
                                                    'magnitude'])

    plotter.add_air_station_marker_with_graph(air_data_df)
    plotter.generate_map()
    return redirect('/measurements/show')


def show_map():
    return render_template('measurements/show.html')


def delete_measurements():
    measurements = Measurement.query
    for measurement in measurements:
        db.session.delete(measurement)

    db.session.commit()
    return redirect('/measurements')