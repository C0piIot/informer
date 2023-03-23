FROM python:slim AS base
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends git python3-lxml
RUN pip install --upgrade pip
COPY requirements.txt package.json yarn.lock /app/
RUN apt-get install -y libxml2-dev libxslt-dev python-dev build-essential zlib1g-dev yarnpkg &&\
	pip install --no-cache-dir -r requirements.txt &&\
	apt-get autoremove -y --purge libxml2-dev libxslt-dev python-dev build-essential
RUN yarnpkg install
ARG BUILD_VERSION=dev
ENV BUILD_VERSION=$BUILD_VERSION
ARG GIT_REV=HEAD
ENV GIT_REV=$GIT_REV


FROM base AS dev
COPY requirements-dev.txt /app/
RUN pip install --no-cache-dir -r requirements-dev.txt

FROM base AS prod
COPY . /app/
RUN pip install --no-cache-dir -r requirements-prod.txt
RUN python manage.py collectstatic --no-input

FROM dev AS trendier
COPY requirements-trendier.txt /app/
RUN apt-get install -y python-dev build-essential &&\
	pip install --no-cache-dir -r requirements-trendier.txt &&\
	apt-get autoremove -y --purge python-dev build-essential

RUN pip install mysql-connector-python boto3