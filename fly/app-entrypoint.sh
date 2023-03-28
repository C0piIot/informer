#!/bin/bash
fallocate -l 128M /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
newrelic-admin run-program uwsgi /app/fly/uwsgi.ini
