from app import db

class StationDuplicate(db.Model):
    #__table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    start_date= db.Column(db.Date(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200))
    latitude = db.Column(db.FLOAT, nullable=False)
    longitude = db.Column(db.FLOAT, nullable=False)
    altitude = db.Column(db.FLOAT)
    changed_name = db.Column(db.BOOLEAN)
    changed_type = db.Column(db.BOOLEAN)
    changed_address = db.Column(db.BOOLEAN)
    changed_latitude = db.Column(db.BOOLEAN)
    changed_longitude = db.Column(db.BOOLEAN)
