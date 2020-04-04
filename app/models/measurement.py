from app import db
import pandas as pd
from datetime import date


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

    def read_measurement_file(self, measurementFile):
        """Esta función se encarga de leer todos los archivos en el directorio que cumplen
        con el criterio de la extención"""
        print('I am in the correct function here, good job and continue')
        tmp = []

        self.maintable = self.__read_csv_data(measurementFile)
        for index, row in self.maintable.iterrows():
            tmp.append([row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5]])

        self.maintable = tmp
        print('HEy PILAS CA CON ESTA LIENA :', type(tmp))

    def __read_csv_data(self, magnitudeFile):
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

        return self.prepare_data(measurement)

    def prepare_data(self, datos):
        # logging.info('Reshaping data: {}'.format(file_name))
        datos = datos.astype({'MAGNITUD': int})
        datos = datos[(datos.MAGNITUD == 6)]

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

        # Pasar la hora formato datetime
        data_3 = data_3.astype({'HORA': int, 'PUNTO_MUESTREO': int})
        data_3.HORA = data_3.HORA - 1

        # Sea agrega una columna que puede servir como indice.
        data_3['TIMESTAMP'] = 0

        data_3['TIMESTAMP'] = data_3.apply(lambda fila: self.__process_timestamp(fila), axis=1)

        # Reorganizar las columnas para a justarse a el modelo de la base de datos
        data_3 = self.__reorder_columns(data_3)

        # logging.info('Done reshaping data: {} - Data shape: {}'.format(file_name, str(data_3.shape)))
        return data_3

    def __process_timestamp(self, fila):
        # return pd.datetime(fila.ANO, fila.MES, fila.DIA)
        if fila.MES < 10:
            fila.MES = '0' + str(fila.MES)

        else:
            fila.MES = str(file.MES)

        if fila.DIA < 10:
            fila.DIA = '0' + str(fila.DIA)

        else:
            fila.DIA = str(fila.DIA)

        return int(''.join([str(fila.ANO), fila.MES, fila.DIA]))

    def __reorder_columns(self, table):
        table = table[['PUNTO_MUESTREO', 'TIMESTAMP', 'HORA', 'MAGNITUD', 'VALOR', 'VALIDEZ']]
        return table
