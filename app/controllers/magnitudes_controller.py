from flask import render_template, request, redirect
from flask_paginate import Pagination, get_page_args
from app.models.magnitude import Magnitude
from app import db

#@magnitudes_blueprints.route('/')
def index_magnitudes():
    magnitudes = Magnitude.query.order_by(Magnitude.id)
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    pagination_magnitudes = magnitudes[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=magnitudes.count(), css_framework='bootstrap4')
    return render_template('magnitudes/index.html', magnitudes=pagination_magnitudes, page=page, per_page=per_page, pagination=pagination)

def create_magnitudes():
    magnitudes = Magnitude.read_magnitude_file(request.files['file'], request.form.get('magnitudeCategory'))
    for magnitude in magnitudes:
        new_magnitude = Magnitude(id=magnitude[0], name=magnitude[1], abbreviation=magnitude[2],
                              unit=magnitude[3], max_value_excelent=magnitude[4],
                              min_value_good=magnitude[5], max_value_good=magnitude[6],
                              min_value_acceptable=magnitude[7], max_value_acceptable=magnitude[8],
                              min_value_bad=magnitude[9], category=magnitude[10])
        magnitude = Magnitude.query.get(magnitude[0])
        if magnitude:
            continue
        db.session.add(new_magnitude)
        db.session.commit()
    return redirect('/magnitudes')

def delete_magnitudes():
    db.session.query(Magnitude).delete()
    db.session.commit()
    return redirect('/magnitudes')
