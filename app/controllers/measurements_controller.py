from flask import render_template, request, redirect
from app.models.measurement import Measurement, FileReader
from app import db


# @measurements_blueprints.route('/')
def index_measurements():
    measurements = Measurement.query
    return render_template('measurements/index.html', measurements=measurements)


def create_measurements():
    measurement_obj = FileReader()
    measurement_obj.read_measurement_file(request.files['file'])

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


def delete_measurements():
    pass
