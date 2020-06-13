from flask import render_template, request, redirect
from flask_paginate import Pagination, get_page_args
from app.models.day import Day
from app import db

#@dates_blueprints.route('/')
def index_days():
    days = Day.query.order_by(Day.id)
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    pagination_days = days[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=days.count(), css_framework='bootstrap4')
    return render_template('days/index.html', days=pagination_days, page=page, per_page=per_page, pagination=pagination)

def create_days():
    days = Day.create_range(request.form.get('initialDay'), request.form.get('finalDay'))
    for day in days:
        new_day = Day(id=''.join(day), day=day[2], month=day[1], year=day[0])
        day = Day.query.get(''.join(day))
        if day:
            continue
        db.session.add(new_day)
        db.session.commit()
    return redirect('/days')

def delete_days():
    db.session.query(Day).delete()
    db.session.commit()
    return redirect('/days')
