#!/bin/bash
./manage.py get_walking_times &
wait
./scripts/query.sh &
QPID=$!
./manage.py runserver
kill $QPID