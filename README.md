# Madrid Central Web application

Web application to load the datasets for the Madrid Central project.

## Requirements

* docker
* docker-compose

## Installation

```bash
docker-compose build
```

## Running the App

To run the app in development mode, execute:
```bash
docker-compose up
```

## Access the DB

```bash
docker-compose exec db psql -U postgres -d madrid_central
```

## Create madrid_central tables

Execute `1.CREATEDATABASE.sql` 

## Running the app to use debug breakpoints
```bash
docker-compose run -p 5000:5000 app
```

and then open `http://localhost:5000`

## How to install new python libs

After adding the new library to the `requirements.txt` file, run:

```bash
docker-compose exec app pip install -r requirements.txt
```

## Create tables with SQLAlchemy

```bash
docker-compose exec app python
from app import db, create_app
db.create_all(app=create_app())
```
