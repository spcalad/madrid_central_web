from app import db
import pandas as pd

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def create_range(initialDay, finalDay):
        day_rng = list(pd.date_range(start=initialDay, end=finalDay, freq='D'))
        days = []

        for fila in day_rng:
            days.append(str(fila).split(' ')[0].split('-'))

        return days
