#!/bin/bash

source /vagrant/virtualenvs/dbasik/bin/activate
cd /vagrant/code/dbasik_dftgovernance
python manage.py runserver 0.0.0.0:8000 --settings=config.settings.staging
