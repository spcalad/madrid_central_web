from flask import render_template, request, redirect
from app.models.classificator import Classificator
from app import db

#@classificators_blueprints.route('/')
def index_classificators():
    plot = Classificator.generate_plot()
    img = f'data:image/png;base64,{plot.decode("utf8")}'

    return render_template('classificator/index.html', img=img)

def create_classificators():
    Classificator.generate_classification()
    return redirect('/classificators')
