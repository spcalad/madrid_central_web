from app import db
import pandas as pd
from pyproj import Proj
import re


class Station(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    type = db.Column(db.String(40))
    address = db.Column(db.String(40))
    latitude = db.Column(db.FLOAT, nullable=False)
    longitude = db.Column(db.FLOAT, nullable=False)
    altitude = db.Column(db.FLOAT)
    start_date = db.Column(db.Date())
    category = db.Column(db.String(10))

    def read_stations_file(stationsFile, stationCategory):
        stations = pd.read_csv(stationsFile,
                               sep=';',
                               header='infer',
                               encoding='iso-8859-1')

        stations = stations[
            ['CODIGO', 'ESTACION', 'COD_TIPO', 'DIRECCION', 'LATITUD', 'LONGITUD', 'ALTITUD', 'Fecha alta']]

        stations['Fecha alta'] = pd.to_datetime(stations['Fecha alta'][0])
        stations['Category'] = 'CA'

        # elif stationCategory == 'transito':
        # breakpoint()
        # stations = stations[['idelem', 'identif', 'tipo_elem', 'nombre', 'st_x', 'st_y']]
        # stations[['tipo_elem']] = stations.tipo_elem.replace({'PUNTOS DE MEDIDA URBANOS': 'URB', 'PUNTOS DE MEDIDA M-30': 'M30'})
        # stations[['st_x']] = str(stations.st_x).replace('.', '')
        #
        #
        # stations[['st_x']] = stations(lambda x: re.sub(r',', '.', x.st_x))
        # #to_latlon(340000, 5710000, 32, 'U')
        #
        #
        #
        # stations['Category'] = 'T'

        return stations.values
