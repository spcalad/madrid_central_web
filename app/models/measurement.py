from app import db
import pandas as pd
from datetime import date
import io
import folium
import vincent


class Measurement(db.Model):
    __table_args__ = {'extend_existing': True}
    station_id = db.Column(db.Integer, primary_key=True)
    day_id = db.Column(db.Integer, primary_key=True)
    time_id = db.Column(db.Integer, primary_key=True)
    magnitude_id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.FLOAT, nullable=True)
    validation = db.Column(db.String(1), nullable=True)


class FileReader:
    def __init__(self):
        self.maintable = []
        self.extension = dict(csv='.csv', txt='.txt')

    def read_measurement_file(self, measurementFile):
        """Esta función se encarga de leer todos los archivos en el directorio que cumplen
        con el criterio de la extención"""
        tmp = []
        print(measurementFile.filename)
        try:
            # print(measurementFile.__dict__)
            ext_file = measurementFile.filename[-4:]
            if ext_file == self.extension['csv']:
                self.maintable = self._read_csv_data(measurementFile)

            elif ext_file == self.extension['txt']:
                self.maintable = self._read_txt_files(measurementFile)

        except Exception as e:
            print(
                f'An exception has raised while reading the csv file - Can not read the file: {measurementFile.filename}')
            print('Exception: {0} - {1} - {2}'.format(e, e.__traceback__.tb_frame, e.__traceback__.tb_lineno))
            self.maintable = []

        if len(self.maintable) != 0:
            for index, row in self.maintable.iterrows():
                tmp.append([row[0],
                            row[1],
                            row[2],
                            row[3],
                            row[4],
                            row[5]])

            self.maintable = tmp
            return True

        else:
            return False

    def _read_csv_data(self, magnitudeFile):
        measurement = pd.read_csv(magnitudeFile,
                                  header='infer',
                                  sep=';',
                                  encoding='iso-8859-1')

        tmp = pd.DataFrame(measurement['PUNTO_MUESTREO'])
        tmp['TECNICA_MUESTREO'] = 0
        for fila in range(0, len(tmp)):
            tmp.iloc[fila, 1] = str.split(tmp.iloc[fila, 0], "_")[2]
            tmp.iloc[fila, 0] = str.split(tmp.iloc[fila, 0], "_")[0]

        # Se asignan las columnas nuevas al DataFrame general.
        measurement['PUNTO_MUESTREO'] = tmp['PUNTO_MUESTREO']
        measurement.insert(5, 'TECNICA_MUESTREO', tmp['TECNICA_MUESTREO'])

        return self._prepare_data(measurement)

    def _read_txt_files(self, magnitudeFile):
        """Esta función se encarga de leer los archiivos de tipo .txt y
        prepararlos para la carga"""
        # logging.info('Reading and process data...')
        try:
            bytes_data = magnitudeFile.read()
            str_memory_file = bytes_data.decode('iso-8859-1')
            datos = io.StringIO(str_memory_file)
            contador = 0
            splitters = [2, 5, 8, 10, 12, 14, 16, 18, 20, 22]
            lst = []
            while True:
                temporal_row = []
                _ = datos.readline()
                if not _:
                    # logging.info('Done: ' + str(contador) + ' processed')
                    break

                for spl in range(0, len(splitters)):
                    if spl == 0:
                        temporal_row.append(_[0:splitters[spl]])

                    else:
                        if spl == 3:
                            # print('spl = ', str(spl))
                            concat_str = temporal_row[0] + temporal_row[1] + temporal_row[2]
                            temporal_row.append(_[splitters[spl - 1]:splitters[spl]])
                            temporal_row.append(concat_str)

                        elif spl == len(splitters) - 1:
                            # print('spl = ', str(spl))
                            tmp_values = _[splitters[spl - 1]:]

                            for i in range(1, 25):
                                if i == 1:
                                    v = tmp_values[0:(i * 6)]
                                    temporal_row.append(v[0:5])
                                    temporal_row.append(v[5:6])

                                else:
                                    v = tmp_values[((i - 1) * 6):(i * 6)]
                                    temporal_row.append(v[0:5])
                                    temporal_row.append(v[5:6])

                        elif spl == 6:
                            # print('spl = ', str(spl), _[splitters[spl - 1]:splitters[spl]])
                            temporal_row.append('20' + _[splitters[spl - 1]:splitters[spl]])

                        else:
                            # print('spl = ', str(spl), _[splitters[spl - 1]:splitters[spl]], '*')
                            temporal_row.append(_[splitters[spl - 1]:splitters[spl]])

                temporal_row.pop(6)
                contador += 1
                lst.append(temporal_row)

        except Exception as e:
            print('Exception: {0} - {1} - {2}'.format(e, e.__traceback__.tb_frame, e.__traceback__.tb_lineno))

        try:
            column_names = ['PROVINCIA', 'MUNICIPIO', 'ESTACION', 'MAGNITUD', 'PUNTO_MUESTREO', 'TECNICA_MUESTREO',
                            'ANO', 'MES', 'DIA',
                            'H01', 'V01', 'H02', 'V02', 'H03', 'V03', 'H04', 'V04', 'H05', 'V05', 'H06', 'V06', 'H07',
                            'V07', 'H08', 'V08', 'H09', 'V09', 'H10', 'V10', 'H11', 'V11', 'H12', 'V12', 'H13', 'V13',
                            'H14', 'V14', 'H15', 'V15', 'H16', 'V16', 'H17', 'V17', 'H18', 'V18', 'H19', 'V19', 'H20',
                            'V20', 'H21', 'V21', 'H22', 'V22', 'H23', 'V23', 'H24', 'V24']

            final_data = pd.DataFrame(lst, columns=column_names)
            final_data = final_data.astype({'MES': int, 'DIA': int})

        except Exception as e:
            print('Exception: {0} - {1} - {2}'.format(e, e.__traceback__.tb_frame, e.__traceback__.tb_lineno))

        return self._prepare_data(final_data)

    def _prepare_data(self, datos):
        datos = datos.astype({'MAGNITUD': int})
        datos = datos[(datos.MAGNITUD == 14) |
                      (datos.MAGNITUD == 8) |
                      (datos.MAGNITUD == 9) |
                      (datos.MAGNITUD == 10)]

        # Preparación de la tabla de datos
        col_names = datos.columns
        col_comunes = list(col_names[0:9])
        col_names_1 = list(col_names[9::2])
        col_names_2 = list(col_names[10::2])

        data_1 = datos[col_comunes + col_names_1]
        data_2 = datos[col_comunes + col_names_2]

        data_long_1 = data_1.melt(id_vars=col_comunes,
                                  var_name='HORA',
                                  value_name='VALOR')

        data_long_2 = data_2.melt(id_vars=col_comunes,
                                  var_name='HORA',
                                  value_name='VALIDEZ')

        data_long_1['HORA'] = data_long_1.HORA.str.replace('H', '')
        data_long_2['HORA'] = data_long_2.HORA.str.replace('V', '')

        # Operación de merge con la que se obtiene la tabla final para comerzar
        # a realizar las operaciones.
        data_3 = data_long_1.merge(data_long_2, how='inner', on=col_comunes + ['HORA'])

        # process validation character
        data_3.VALIDEZ = data_3.apply(lambda row: self._process_validation(row), axis=1)

        # Pasar la hora formato datetime
        data_3 = data_3.astype({'HORA': int, 'PUNTO_MUESTREO': int})
        data_3.HORA = data_3.HORA - 1

        # Sea agrega una columna que puede servir como indice.
        data_3['TIMESTAMP'] = 0

        data_3['TIMESTAMP'] = data_3.apply(lambda fila: self._process_timestamp(fila), axis=1)

        # Reorganizar las columnas para a justarse a el modelo de la base de datos
        data_3 = self._reorder_columns(data_3)

        # logging.info('Done reshaping data: {} - Data shape: {}'.format(file_name, str(data_3.shape)))
        return data_3

    def _process_timestamp(self, fila):
        """Esta función se encarga de juntar las filas AÑO MES DIA para formar el campo day_id de la tabla measurement"""
        if fila.MES < 10:
            fila.MES = '0' + str(fila.MES)

        else:
            fila.MES = str(fila.MES)

        if fila.DIA < 10:
            fila.DIA = '0' + str(fila.DIA)

        else:
            fila.DIA = str(fila.DIA)

        return int(''.join([str(fila.ANO), fila.MES, fila.DIA]))

    def _reorder_columns(self, table):
        """Esta función se encarga de seleccionar y reorganiar las columnas del DataFrame. El orden es el mismo de
        la tabla measurement en la base de datos"""
        table = table[['PUNTO_MUESTREO', 'TIMESTAMP', 'HORA', 'MAGNITUD', 'VALOR', 'VALIDEZ']]
        return table

    def _process_validation(self, row):
        if row.VALIDEZ == 'V':
            return 't'
        else:
            return 'f'

    def read_traffic_file(self, magnitudeFile):
        try:
            traffic = pd.read_csv(magnitudeFile,
                                  header='infer',
                                  sep=';',
                                  encoding='iso-8859-1')

            traffic['day_id'] = traffic.apply(lambda row: row.day_id.replace('-', ''), axis=1)
            traffic.drop(columns=['Unnamed: 0'], inplace=True)
            print(traffic.head())
            self.maintable = list(traffic.values)
            return True

        except Exception as e:
            print(
                f'An exception has raised while reading the csv file - Can not read the file: {measurementFile.filename}')
            print('Exception: {0} - {1} - {2}'.format(e, e.__traceback__.tb_frame, e.__traceback__.tb_lineno))
            return False


class Plotter:
    """Esta clase contiene todos los metodos y las operaciones necesarias para generar mapas"""

    COORDENADAS_MADRID = [40.4167598, -3.7040395]
    ZOOM_START = 13

    def __init__(self, location=COORDENADAS_MADRID, zoom=ZOOM_START):
        self._zoom = zoom
        self._location = location
        self._map = self.__initialize_map()

    @property
    def zoom(self):
        return self._location

    @zoom.setter
    def zoom(self, value):
        if value < 1 or value > 17:
            raise ValueError('Zoom no permitido. Pruebe con un valor en el rango 1 - 16')

        else:
            self._location = value

    @property
    def map(self):
        return self._map

    @map.setter
    def map(self, value):
        if isinstance(value, folium.folium.Map):
            self._map = value

        else:
            raise ValueError('The value must be an d instance of the class folium.Map()')

    def __initialize_map(self):
        """Inicializa in mapa con centro en las coordenadas de Madrid con el polígono que delimita Madrid Central"""

        m = folium.Map(location=self.COORDENADAS_MADRID,
                       tiles='OpenStreetMap',
                       zoom_start=self.ZOOM_START)

        gj = folium.GeoJson(data={
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-3.711305, 40.406807],
                    [-3.702612, 40.404997],
                    [-3.693235, 40.407742],
                    [-3.692248, 40.409000],
                    [-3.694617, 40.415505],
                    [-3.690392, 40.424887],
                    [-3.696207, 40.427856],
                    [-3.702162, 40.429122],
                    [-3.705810, 40.429681],
                    [-3.714018, 40.430404],
                    [-3.715059, 40.428918],
                    [-3.711797, 40.424377],
                    [-3.714372, 40.422988],
                    [-3.712870, 40.421534],
                    [-3.714029, 40.410539]
                ]]
            }
        }, name="Madrid Central")

        gj.add_child(folium.Popup('Área de Madrid Central'))
        gj.add_to(m)
        folium.LayerControl().add_to(m)
        return m

    def add_air_station_marker(self, locations, station_names=None, legend=None, **kwargs):
        """Agrega al mapa el tantas estaciones de calidad del aire como ubicaciones existan dentro del parametro
        locations"""
        if station_names is None:
            station_names = [[i] for i in range(len(locations))]

        for location, stat_name in zip(locations, station_names):
            try:
                folium.Marker(location=location,
                              tooltip=folium.Tooltip(
                                  f'Estación: {stat_name[0]}<br>Latitud: {round(location[0], 4)}<br>Longitud: {round(location[1], 4)}'),
                              popup=legend,
                              icon=folium.CustomIcon(icon_image='app/views/icons/forecast.png',
                                                     icon_size=(40, 40))).add_to(self._map)
            except TypeError as e:
                print("El parametro location debe ser un de la forma [lat, lon] ó (lat,lon)")
                print('Probando con la siguiente estación...')
                continue

            except FileNotFoundError as e:
                print('El archivo para representar las estaciones no se encuentra en la carpeta "icons"')
                break

            except Exception as e:
                print(e)

    def add_air_station_marker_with_graph(self, data, *args, **kwargs):
        """Esta función se encarga de agregar graficos al los marcadores existentes"""
        locations = data.iloc[:, [1, 2]]
        station_names = data.iloc[:, [3]]

        station_ids = list(pd.unique(data.id))
        station_groups = data.groupby('id')

        for id in station_ids:
            filtered_data = station_groups.get_group(id)
            print('***** data get group')
            print(type(filtered_data))
            print(filtered_data.head())
            plot_data = filtered_data.groupby(['magnitude', 'year', 'month', 'day']).agg(
                {'value': 'mean'}).reset_index()
            print('***** data plot data')
            print(type(plot_data))
            print(plot_data.head())

            x = [int(hour) for hour in list(plot_data['day'])]
            y = [int(value) for value in list(plot_data['value'])]
            print(x)
            print(y)

            xy_values = {
                'x': x,
                'y': y,
            }
            scatter_chart = vincent.Scatter(xy_values,
                                            iter_idx='x',
                                            width=600,
                                            height=300)

            scatter_chart.axis_titles(x='Día', y='Promedio Dióxido de Nitrogeno día')

            popup_scatter_plot = folium.Popup(max_width=900).add_child(
                folium.Vega(scatter_chart, height=350, width=700))

            air_quality_station = [filtered_data.iloc[0, 1], filtered_data.iloc[0, 2]]
            print(air_quality_station)
            station_name = [filtered_data.iloc[0, 3]]
            print(station_name)
            folium.Marker(location=air_quality_station,
                          tooltip=folium.Tooltip(
                              f'Estación: {station_name[0]}<br>Latitud: {round(air_quality_station[0], 4)}<br>Longitud: {round(air_quality_station[1], 4)}'),
                          popup=popup_scatter_plot,
                          icon=folium.CustomIcon(icon_image='app/views/icons/forecast.png',
                                                 icon_size=(40, 40))).add_to(self._map)

    def generate_map(self):
        self.map.save('app/views/test_out/map.html')