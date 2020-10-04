#! /bin/bash
uwsgi /var/www/backend/uwsgi.ini & service nginx start
/bin/sh -c "while sleep 1000; do :; done"