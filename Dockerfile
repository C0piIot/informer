FROM python:slim
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y --no-install-recommends redis python3-dev build-essential git
COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
RUN python manage.py collectstatic --no-input
CMD ["bash", "/usr/src/app/entrypoint.sh"]