#!/bin/sh
#docker-compose exec -T informer_app autoflake -r --in-place --remove-unused-variables --remove-all-unused-imports /app
docker-compose exec -T informer_app isort /app
docker-compose exec -T informer_app ssort /app
docker-compose exec -T informer_app autopep8 --in-place -r --experimental /app
docker-compose exec -T informer_app pylint --rcfile /app/pylintrc --recursive=y /app
