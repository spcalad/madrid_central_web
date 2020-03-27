from flask import render_template, request, redirect
from app.models.magnitude import Magnitude
from app import db

#@magnitudes_blueprints.route('/')
def index_magnitudes():
    magnitudes = Magnitude.query
    return render_template('magnitudes/index.html', magnitudes=magnitudes)

def create_magnitude():
    new_magnitude = Magnitude(id=request.form.get('id'), name=request.form.get('name'), abbreviation=request.form.get('abbreviation'),
                              unit=request.form.get('unit'), max_value_excelent=request.form.get('max_value_excelent'),
                              min_value_good=request.form.get('min_value_good'), max_value_good=request.form.get('max_value_good'),
                              min_value_acceptable=request.form.get('min_value_acceptable'), max_value_acceptable=request.form.get('max_value_acceptable'),
                              min_value_bad=request.form.get('min_value_bad'))

    db.session.add(new_magnitude)
    db.session.commit()
    return redirect('/magnitudes')

def delete_magnitudes():
    magnitudes = Magnitude.query
    for magnitude in magnitudes:
         db.session.delete(magnitude)
         db.session.commit()
    return redirect('/magnitudes')
