#!/bin/bash

NAME="dbasik_dftgovernance"                                  # Name of the application
DJANGODIR=/dbasik/code/dbasik_dftgovernance/             # Django project directory
SOCKFILE=/dbasik/code/run/gunicorn.sock  # we will communicte using this unix socket
USER=dbasik                                       # the user to run as
GROUP=dbasik                                     # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=config.settings.deploy             # which settings file should Django use
DJANGO_WSGI_MODULE=config.wsgi                    # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /dbasik/virtualenvs/dbasik/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /dbasik/virtualenvs/dbasik/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
