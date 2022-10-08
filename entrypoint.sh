#!/bin/bash

if [[ ! -z "$SWAP" ]]; then fallocate -l 64M swapfile && chmod 600 swapfile && mkswap swapfile && swapon swapfile && ls -hla; fi;

python manage.py migrate
sqlite3 /usr/src/app/db.sqlite3 < /usr/src/app/pragma.sql

redis-server --maxmemory 32M &
python manage.py rundramatiq &
uwsgi /usr/src/app/uwsgi.ini
