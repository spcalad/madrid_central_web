from app import db

class Magnitude(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	abbreviation = db.Column(db.String(10), nullable=False)
	unit = db.Column(db.String(10), nullable=False)
	max_value_excelent = db.Column(db.FLOAT, nullable=True)
	min_value_good = db.Column(db.FLOAT, nullable=True)
	max_value_good = db.Column(db.FLOAT, nullable=True)
	min_value_acceptable = db.Column(db.FLOAT, nullable=True)
	max_value_acceptable = db.Column(db.FLOAT, nullable=True)
	min_value_bad = db.Column(db.FLOAT, nullable=True)
