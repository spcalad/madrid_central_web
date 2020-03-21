from app import db


class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def create_range():
        breakpoint()


# script para llenar la tabla day
# date_rng = list(pd.date_range(start='2016/01/01', end='2019/10/31', freq='D'))
# tmp = []
#
# for fila in date_rng:
#     tmp.append(str(fila).split(' ')[0].split('-'))
#
# print(tmp)
#
# for i in range(0, len(tmp)):
#     for j in range(0, len(tmp[i])):
#         tmp[i][j] = str(int(tmp[i][j]))
#
# print(tmp)
#
# for dat in tmp:
#     key = ''.join(dat)
#     dat.insert(0, int(key))
#     print(dat, '*****')
#     dbController.insert('day', dat)
#
# print('finish')
