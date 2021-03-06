from app import db
from sqlalchemy import between, or_
import pandas as pd
import numpy as np
import base64
from io import BytesIO
from sklearn import datasets
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from app.models.station import Station

class Classificator():

    def generate_plot():
        traffic = Classificator.__get_traffic_plot__()
        air_quality = Classificator.__get_air_quality_plot__()
        plt.scatter(traffic.longitude, traffic.latitude, c=traffic.classificator, alpha=0.8, s=64, edgecolors='white')
        plt.scatter(air_quality.longitude, air_quality.latitude, c=air_quality.classificator, marker='s', s=100, edgecolors='black')

        image = BytesIO()
        plt.savefig(image, format='png')
        plt.close()

        return base64.encodestring(image.getvalue())

    def generate_classification():
        iteration = 0
        K = Classificator.__get_clusters__(iteration)
        lat_long = Classificator.__get_coordinates__().to_numpy()

        Classificator.__classify__(K, lat_long)
        iteration += 1

        K= Classificator.__get_clusters__(iteration)
        Classificator.__classify__(K, lat_long)

    def __get_clusters__(iteration):
        if iteration >= 1:
            return Station.query.filter(Station.category == 'CA', Station.type.in_(['UT', 'UF'])).filter(or_(~Station.latitude.between(40.404997, 40.430404), ~Station.longitude.between(-3.715059, -3.690392))).distinct(Station.classificator).count()
        else:
            return Station.query.filter(Station.category == 'CA', Station.type.in_(['UT', 'UF'])).filter(or_(~Station.latitude.between(40.404997, 40.430404), ~Station.longitude.between(-3.715059, -3.690392))).count()

    def __get_coordinates__():
        return pd.read_sql("""SELECT latitude, longitude
                              FROM station
                              WHERE type IN ('URB', 'UT', 'UF')
                              AND latitude != 'NaN'
                              AND longitude != 'NaN'
                              AND NOT ((latitude BETWEEN 40.404997 AND 40.430404) AND (longitude BETWEEN -3.715059 AND -3.690392))
                              ORDER BY id""", db.engine)

    def __get_stations__():
        return Station.query.filter(Station.type.in_(['URB', 'UT', 'UF']), Station.latitude != 'NaN', Station.longitude != 'NaN').filter(or_(~Station.latitude.between(40.404997, 40.430404), ~Station.longitude.between(-3.715059, -3.690392))).order_by(Station.id).all()

    def __classify__(K, lat_long):
        km = KMeans(n_clusters=K)
        labels = km.fit(lat_long).labels_

        stations = Classificator.__get_stations__()

        for i in range(len(stations)):
            station = stations[i]
            station.classificator = int(labels[i])+1
        db.session.commit()

        db.session.query(Station).filter(Station.type.in_(['URB', 'UT', 'UF']), Station.latitude != 'NaN', Station.longitude != 'NaN', Station.latitude.between(40.404997, 40.430404), Station.longitude.between(-3.715059, -3.690392)).update(values={"classificator": 0}, synchronize_session=False)
        db.session.commit()

    def __get_traffic_plot__():
        return pd.read_sql("""SELECT latitude, longitude, classificator
                              FROM station
                              WHERE category = 'T'
                              AND type = 'URB'
                              AND latitude != 'NaN'
                              AND longitude != 'NaN'""", db.engine)

    def __get_air_quality_plot__():
        return pd.read_sql("""SELECT latitude, longitude, classificator
                              FROM station
                              WHERE category = 'CA' AND type IN ('UT', 'UF')""", db.engine)
