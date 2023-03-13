#!/bin/sh
docker-compose exec -T informer_app autoflake -r --in-place --remove-unused-variables /app
docker-compose exec -T informer_app isort /app
docker-compose exec -T informer_app ssort /app
docker-compose exec -T informer_app autopep8 --in-place -r /app
