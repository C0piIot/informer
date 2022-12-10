FROM python:slim AS base
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y --no-install-recommends redis git sqlite3 python3-lxml
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app
RUN apt-get install -y libxml2-dev libxslt-dev python-dev build-essential zlib1g-dev &&\
	pip install --no-cache-dir -r requirements.txt &&\
	apt-get autoremove -y --purge libxml2-dev libxslt-dev python-dev build-essential

FROM base AS dev
COPY requirements-dev.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements-dev.txt

FROM base AS prod
COPY . /usr/src/app
RUN python manage.py collectstatic --no-input

CMD ["bash", "/usr/src/app/entrypoint.sh"]
