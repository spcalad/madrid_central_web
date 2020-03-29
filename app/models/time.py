from app import db
import pandas as pd

class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hour = db.Column(db.Integer, nullable=False)

    def create_interval(initialTime, finalTime):
        time = list(range(int(initialTime[0:2]), int(finalTime[0:2])+1))

        return time
