FROM python:slim AS base
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y --no-install-recommends redis python3-dev build-essential git sqlite3
RUN pip install --upgrade pip

FROM base AS dev
COPY requirements.txt /usr/src/app
COPY requirements-dev.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements-dev.txt

FROM base AS prod
COPY . /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --no-input

CMD ["bash", "/usr/src/app/entrypoint.sh"]