#!/bin/sh
docker-compose exec -T informer_app autoflake -r --in-place --remove-unused-variables /app
