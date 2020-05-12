from app import db
import pandas as pd
from pyproj import Proj
import re

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    type = db.Column(db.String(40), nullable=False)
    address = db.Column(db.String(40))
    latitude = db.Column(db.FLOAT, nullable=False)
    longitude = db.Column(db.FLOAT, nullable=False)
    altitude = db.Column(db.FLOAT)
    start_date= db.Column(db.Date())
    category = db.Column(db.String(10), nullable=False)

    def read_stations_file(stationsFile, stationCategory, monthFile, yearFile):
        filePath = "/tmp/stations.csv"
        stationsFile.save(filePath)

        file = open(filePath, encoding='iso-8859-1')

        stations = pd.read_csv(file,
            sep=';',
            header='infer',
            error_bad_lines=False)
        if stationCategory == 'aire':
            stations = stations[['CODIGO', 'ESTACION', 'COD_TIPO', 'DIRECCION', 'LATITUD', 'LONGITUD', 'ALTITUD', 'Fecha alta']]
            stations['Fecha alta'] = pd.to_datetime(stations['Fecha alta'][0])
            stations['Category'] = 'CA'

        elif stationCategory == 'transito':
            stations[['tipo_elem']] = stations.tipo_elem.replace({'PUNTOS DE MEDIDA URBANOS': 'URB', 'PUNTOS DE MEDIDA M-30': 'M30'})
            stations[['tipo_elem']] = stations.tipo_elem.replace({'URBANOS': 'URB', 'M-30': 'M30'})
            stations.columns = stations.columns.str.replace('identif', 'cod_cent')
            stations.columns = stations.columns.str.replace('idelem', 'id')
            stations['Category'] = 'T'
            stations['altitude'] = '0'
            monthFile = Station.month_converter(monthFile)
            stations['start_date'] = pd.to_datetime(str(monthFile)+'-'+yearFile)
            stations['id'] = stations.apply(lambda x: str(x.id)+str(monthFile)+str(yearFile), axis=1)

            if 'longitud' not in stations.columns and 'latitud' not in stations.columns:
                stations = Station.convert_coordinates(stations)

            stations = stations[['id', 'cod_cent', 'tipo_elem', 'nombre', 'latitud', 'longitud', 'altitude', 'start_date', 'Category']]

        return stations.values

    def convert_coordinates(stations):
        stations[['st_x']] = stations.st_x.str.replace('.', '')
        stations[['st_x']] = stations.apply(lambda x: x.st_x[:6] + '.' + x.st_x[6:], axis=1)

        stations[['st_y']] = stations.st_y.str.replace('.', '')
        stations[['st_y']] = stations.apply(lambda y: y.st_y[:7] + '.' + y.st_y[7:], axis=1)

        myProj = Proj("+proj=utm +zone=30T, +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
        stations['longitud'], stations['latitud'] = myProj(stations[['st_x']].values, stations[['st_y']].values, inverse=True)
        return stations

    def month_converter(month):
        months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        return months.index(month) + 1
