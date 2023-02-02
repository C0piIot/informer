#!/bin/bash
fallocate -l 128M /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
python /app/manage.py rundramatiq