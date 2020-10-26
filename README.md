# true-house-be ![CI](https://github.com/gAmadorH/true-house-be/workflows/deploy/badge.svg?branch=main)

TrueHouse backend

## requirements

system requirements

* Python 3.8.5
* postgres 12.4

you can run the app even if you do not have this requirements  
running using docker compose, see `run using docker compose` section  
requirements to run using docker compose

* docker compose 1.27.0

## production dependencies

* Django==2.2.16
* djangorestframework==3.9.2
* django-environ==0.4.5
* psycopg2==2.8.6

## production dependencies

* black==20.8b1
* flake8==3.8.4
* pylint==2.6.0

## run using docker compose

run the the following commands

```bash
git clone https://github.com/gAmadorH/true-house-be.git
cd true-house-be
cd .env.example .env
docker-compose up -d db
docker-compose up -d web
```

now you can access to the app in `http://0.0.0.0:8000`

## run with python

run the the following commands (you need a postgres service running)

```bash
git clone https://github.com/gAmadorH/true-house-be.git
cd true-house-be
cd .env.example .env
python -m pip install --upgrade pip
pip install -r requirements/production.txt
pip install -r requirements/local.txt
python true_house/manage.py migrate
python true_house/manage.py runserver 0.0.0.0:8000
```

now you can access to the app in `http://0.0.0.0:8000`

## lint and quality

you need to have the development requirements installed  
`requirement/local.txt`

```bash
flake8 true_house/
black true_house
python true_house/manage.py test activities.tests
```
