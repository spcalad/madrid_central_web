from flask import render_template, request, redirect
from app.models.magnitude import Magnitude
from app import db

#@magnitudes_blueprints.route('/')
def index_magnitudes():
    magnitudes = Magnitude.query
    return render_template('magnitudes/index.html', magnitudes=magnitudes)

def create_magnitudes():
    magnitudes = Magnitude.read_magnitude_file(request.files['file'])
    for magnitude in magnitudes:
        new_magnitude = Magnitude(id=magnitude[0], name=magnitude[1], abbreviation=magnitude[2],
                              unit=magnitude[3], max_value_excelent=magnitude[4],
                              min_value_good=magnitude[5], max_value_good=magnitude[6],
                              min_value_acceptable=magnitude[7], max_value_acceptable=magnitude[8],
                              min_value_bad=magnitude[9])

        db.session.add(new_magnitude)
        db.session.commit()
    return redirect('/magnitudes')

def delete_magnitudes():
    magnitudes = Magnitude.query
    for magnitude in magnitudes:
         db.session.delete(magnitude)
         db.session.commit()
    return redirect('/magnitudes')
