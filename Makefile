run-staging-server:
	python manage.py runserver 0.0.0.0:8000 --settings=config.settings.staging

clean:
	provision/clean_and_repopulate_database.sh

test:
	pytest --driver Firefox --driver-path /home/lemon/bin/geckodriver --tb=short  -v --ds=config.settings.local --html report.html -sx
