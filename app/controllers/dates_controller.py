from flask import render_template, request, redirect
from app.models.date import Date
import pandas as pd

#@dates_blueprints.route('/')
def index_dates():
    return render_template('dates/index.html')

def create_dates():
    dates = Date.create_range()
    print(request.form.get('initialDate'))
    return redirect('/dates')
