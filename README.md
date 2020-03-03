# Madrid Central Web application

Web application to load the datasets for the Madrid Central project.

## Requirements

* docker
* docker-compose

## Installation

```bash
docker-compose build
```

## Running the app

To run the app in development mode, execute:
```bash
docker-compose up
```

and then open `http://localhost:5000`

## How to install new python libs

After adding the new library to the `requirements.txt` file, run:

```bash
docker-compose exec app pip install -r requirements.txt
```

## How to access to the DB

```bash
docker-compose exec db psql -U postgres -d madrid_central
```

## Create tables with SQLAlchemy

```bash
docker-compose exec app python
from app import db, create_app
db.create_all(app=create_app())
```
