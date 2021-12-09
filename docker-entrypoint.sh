#!/bin/sh
# NOTE: if there is no bash can cause
# standard_init_linux.go:190: exec user process caused "no such file or directory"

# https://docs.docker.com/compose/startup-order/
set -euo pipefail

WAIT_FOR_POSTGRES=${WAIT_FOR_POSTGRES:-true}

if [[ "$WAIT_FOR_POSTGRES" = true ]]; then
    DATABASE_URL=${DATABASE_URL:-postgres://postgres:postgres@postgres:5432/postgres}

    # convert to connection string
    # https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-CONNSTRING
    POSTGRES_URL=${DATABASE_URL%%\?*}
    # https://www.gnu.org/software/bash/manual/bash.html#Shell-Parameter-Expansion
    POSTGRES_URL=${POSTGRES_URL/#postgis:/postgres:}

    # let postgres and other services (e.g. elasticsearch) to warm up...
    # https://www.caktusgroup.com/blog/2017/03/14/production-ready-dockerfile-your-python-django-app/
    until psql $POSTGRES_URL -c '\q'; do
        >&2 echo "Postgres is not available - sleeping"
        sleep 2
    done
    >&2 echo "Postgres is up - executing command"
fi

if [[ $# -ge 1 ]]; then
    exec "$@"
else
    cd /var/www
    echo "Applying migrations"
    python manage.py migrate --noinput -v 1
    echo "Generate translations"
    # python manage.py compilemessages --locale ru -v 0
    echo "Starting server"

    gunicorn intranet.wsgi:application --bind 0.0.0.0:$WEB_PORT --workers 3 --log-level=error --log-file=gunicorn.log
fi
