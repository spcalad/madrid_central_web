from app import db
from app.models.station_duplicate import StationDuplicate
import pandas as pd
from pyproj import Proj
import re

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200))
    latitude = db.Column(db.FLOAT, nullable=False)
    longitude = db.Column(db.FLOAT, nullable=False)
    altitude = db.Column(db.FLOAT)
    start_date = db.Column(db.Date())
    classificator = db.Column(db.Integer)

    def create(newStation):
        station = Station.query.get(newStation.id)
        if station:
            if (station.name != newStation.name or station.type != newStation.type or station.address != newStation.address or station.latitude != newStation.latitude or station.longitude != newStation.longitude) :
                new_station_duplicate = StationDuplicate(id=station.id, name=station.name, type=station.type,
                                      address=station.address, latitude=station.latitude,
                                      longitude=station.longitude, altitude=station.altitude,
                                      start_date=station.start_date, category=station.category,
                                      changed_name=(station.name != newStation.name),
                                      changed_type=(station.type != newStation.type),
                                      changed_address=(station.address != newStation.address),
                                      changed_latitude=(station.latitude != newStation.latitude),
                                      changed_longitude=(station.longitude != newStation.longitude))
                db.session.add(new_station_duplicate)
                db.session.delete(station)
                db.session.add(newStation)
                db.session.commit()
        else:
            db.session.add(newStation)
            db.session.commit()

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
