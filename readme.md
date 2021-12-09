# Settings
### .env file

    DEBUG=True
	SECRET_KEY=arandomstring
	ALLOWED_HOSTS=*,

	DEFAULT_DB_ENGINE=
	DEFAULT_DB_NAME=
	DEFAULT_DB_USER=
	DEFAULT_DB_PWD=
	DEFAULT_DB_HOST=
	DEFAULT_DB_PORT=

	WEB_PORT=8000

## Commands 
### To dev env
	pip install -r requirements-dev.txt
### To prod env
	pip install -r requirements.txt

## Run crawler
    python manage.py crawler

## Run tests
    python manage.py test core.tests

## Run app

    python manage.py runserver


## With Docker

    docker-compose up
