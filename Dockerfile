FROM python:slim
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "informer/manage.py", "runserver", "0.0.0.0:80"]