#!/bin/bash

NAME="laopenacres"
DJANGODIR=$HOME/webapps/laopenacres/livinglots-la/livinglotsla
PORT=<PORT>
USER=laopenacres
GROUP=laopenacres
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=laopenacres.settings.production
DJANGO_WSGI_MODULE=laopenacres.wsgi
VIRTUALENV=laopenacres
LOGDIR=$HOME/webapps/laopenacres/logs

echo "Starting $NAME"

# Activate the virtual environment
source ~/bin/virtualenvwrapper.sh
workon $VIRTUALENV
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE

# Start Django Unicorn
exec gunicorn \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=debug \
  --bind=127.0.0.1:$PORT \
  --log-file $LOGDIR/error.log --access-logfile $LOGDIR/access.log \
  $DJANGO_WSGI_MODULE:application
