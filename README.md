# Traxler

A simple GST management system written in Python.

Please view [this](https://youtu.be/4V2G0QmpLHw) video for a demo / build instructions.

## Tech Stack

- Python 3.10
  - Django as backend
  - django-rest-framework for API
  - authtoken from rest framework for authentication / authorization
- TypeScript
  - Vue 3 for frontend
- PostgreSQL for database
- Docker for containerization
  - alpine as container OS

## Users (pswd: `abcd`)
All users have a password of `abcd` - but each of them have been hashed with argon2. Django takes
care of salting and hashing appropriately.
![users](https://i.imgur.com/2keO4V4.png)

## Installation

### Build

Open a terminal window and run from the root project directory - 

**note - the first startup might take some time to build**

```bash
$ docker-compose up
```
This should start the server. But don't visit the url yet, we need to seed the database.

### Seed database

Open a new terminal and leave the server running. 

To load the fixtures, run - 

```bash
# VERY IMPORTANT - states should be loaded first
$ docker exec traxler-web-1 python manage.py loaddata fixtures/states/data.json

$ docker exec traxler-web-1 python manage.py loaddata fixtures/users/data.json # load users
```

Visit the link provided in the `docker-compose` command - [http://0.0.0.0:8000](http://0.0.0.0:8000) and start exploring!

### Tests

To run tests (make sure the `traxler-web-1` image is still running in another terminal) -

**note - the Unauthorized & Forbidden messages aren't failures**

```bash
$ docker exec traxler-web-1 python manage.py test --keepdb
```