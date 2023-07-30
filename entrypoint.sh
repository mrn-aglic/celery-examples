#!/bin/sh

echo $1

#export example=queue_pub

cd /app/examples || return

if [ "$1" = 'scheduler' ]
then
    exec celery -A ${example}.beat beat --loglevel info
elif [ "$1" = 'worker' ]
then
    exec celery -A ${example}.worker worker -Q "$2" --loglevel info  #--purge # remove purge if you want to use app.control.purge
elif [ "$1" = 'flower' ]
then
    exec celery -A ${example}.worker --broker=redis://redis:6379/0 flower --conf=/config/flowerconfig.py
fi

exec "$@"
