FROM python:3.8-alpine

LABEL maintainer="brunoxbk@gmail.com"

# Set environment varibles
ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8

RUN mkdir -p /var/www

COPY requirements.txt /var/www

WORKDIR /var/www

RUN apk update && apk upgrade

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    apk add build-base python3-dev py-pip jpeg-dev zlib-dev && \
    apk add --no-cache libffi-dev build-base libffi-dev

RUN apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/main openssl \
    build-base cmake musl-dev linux-headers

# RUN apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing gdal-dev

RUN apk add postgresql-client \
    postgresql-dev \
    musl-dev \
    gcc \
    libxml2-dev \
    libxslt-dev \
    linux-headers \
    gettext-dev \
    && apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
    libcrypto1.1 


ENV GEOS_LIBRARY_PATH /usr/lib/libgeos_c.so

RUN pip install -r /var/www/requirements.txt 

COPY docker-entrypoint.sh /

ENTRYPOINT ["sh", "/docker-entrypoint.sh"]

RUN ["chmod", "+x", "/docker-entrypoint.sh"]

COPY . /var/www

WORKDIR /var/www
