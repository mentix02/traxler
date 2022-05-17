# Traxler

A simple GST management system written in Python.

## Tech Stack

- Python 3.10
  - Django as backend
  - django-rest-framework for API
  - authtoken fromm rest framework for authentication / authorization
- TypeScript
  - Vue for frontend
- PostgreSQL for database
- Docker for containerization

## Installation

Open a terminal window and run from the root project directory - 
```shell
docker-compose up
```

This should start the server and initialize the database. 

Open another terminal and run - 

```shell
docker exec traxler-web-1 python manage.py test
```

This will run all Django tests.

To seed database with fixtures, run - 

```shell

# IMPORTANT - load states first
docker exec traxler-web-1 python manage.py loaddata fixtures/states/data.json # loads states

docker exec traxler-web-1 scripts/admin.sh  # creates an admin user
docker exec traxler-web-1 python manage.py loaddata fixtures/users/data.json # loads users
docker exec traxler-web-1 python manage.py loaddata fixtures/taxes/data.json # loads taxes
```
