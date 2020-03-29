from app import db
import pandas as pd

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    type = db.Column(db.String(40), nullable=False)
    address = db.Column(db.String(40), nullable=False)
    latitude = db.Column(db.FLOAT, nullable=False)
    longitude = db.Column(db.FLOAT, nullable=False)
    altitude = db.Column(db.FLOAT, nullable=False)
    start_date= db.Column(db.Date(), nullable=False)

    def read_stations_file(stationsFile):
        stations = pd.read_csv(stationsFile,
             sep=';',
             header='infer',
             encoding='iso-8859-1')

        stations = stations[['CODIGO', 'ESTACION', 'COD_TIPO', 'DIRECCION', 'LATITUD', 'LONGITUD', 'ALTITUD', 'Fecha alta']]
        stations['Fecha alta'] = pd.to_datetime(stations['Fecha alta'][0])

        return stations.values
