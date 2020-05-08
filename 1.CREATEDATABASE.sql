CREATE DATABASE madridcentral;

CREATE TABLE IF NOT EXISTS time(
	id serial PRIMARY KEY,
	hour INT NOT NULL

);
CREATE TABLE IF NOT EXISTS day(
	id serial PRIMARY KEY,
	day INT NOT NULL,
	month INT NOT NULL,
	year INT NOT NULL
);
CREATE TABLE IF NOT EXISTS station(
	id serial PRIMARY KEY, -- pendiente revisar int - string
	name VARCHAR(40) NOT NULL, 
	type VARCHAR(40) NOT NULL,
	category VARCHAR(40) NOT NULL,
	address VARCHAR(200), -- pendiente hacern en postgresql
	latitude FLOAT NOT NULL,
	longitude FLOAT NOT NULL,
	altitude FLOAT,
	start_date DATE
);
CREATE TABLE IF NOT EXISTS magnitude(
	id serial PRIMARY KEY,
	name VARCHAR(50),
	abbreviation VARCHAR(10),
	unit VARCHAR(10),
	max_value_excelent FLOAT,
	min_value_good FLOAT,
	max_value_good FLOAT,
	min_value_acceptable FLOAT,
	max_value_acceptable FLOAT,
	min_value_bad FLOAT
);
CREATE TABLE IF NOT EXISTS measurement(
	station_id INT NOT NULL,
	day_id INT NOT NULL,
	time_id INT NOT NULL,
	magnitude_id INT NOT NULL,
	value FLOAT NOT NULL,
	validation BOOLEAN,
	foreign key(station_id) REFERENCES station(id),
	foreign key(day_id) REFERENCES day(id),
	foreign key(time_id) REFERENCES time(id),
	foreign key(magnitude_id) REFERENCES magnitude(id),
	primary key(station_id, day_id, time_id, magnitude_id)
);
