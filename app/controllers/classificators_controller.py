from flask import render_template, request, redirect
from app.models.classificator import Classificator
from app.models.station import Station
from app import db
from sqlalchemy import update

#@classificators_blueprints.route('/')
def index_classificators():
    plot = Classificator.generate_plot()
    img = f'data:image/png;base64,{plot.decode("utf8")}'

    return render_template('classificators/index.html', img=img)

def create_classificators():
    Classificator.generate_classification()
    return redirect('/classificators')

def delete_classificators():
    db.session.query(Station).update(values={"classificator": None})
    db.session.commit()
    return redirect('/classificators')
