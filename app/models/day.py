from app import db
import pandas as pd

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def create_range(initialDate, finalDate):
        date_rng = list(pd.date_range(start=initialDate, end=finalDate, freq='D'))
        days = []

        for fila in date_rng:
            days.append(str(fila).split(' ')[0].split('-'))

        for i in range(0, len(days)):
            for j in range(0, len(days[i])):
                days[i][j] = str(int(days[i][j]))

        return days
