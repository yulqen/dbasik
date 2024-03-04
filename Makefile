COMPOSEFILE="compose.yaml"
export DBASIK_SECRET_KEY="toss"
CMD=docker compose # this can be overridden on systems that use 'docker compose' plugin rather than 'docker-compose'

up:
	$(CMD) -f $(COMPOSEFILE) up -d web

down:
	$(CMD) -f $(COMPOSEFILE) down

test:
	python manage.py test

clean-rebuild-and-run:
	$(CMD) -f $(COMPOSEFILE) down && $(CMD) -f $(COMPOSEFILE) up --build && $(CMD) -f $(COMPOSEFILE) run web sh -c "python manage.py create_financial_quarters"

createsuperuser:
	$(CMD) -f $(COMPOSEFILE) run --rm web sh -c "python manage.py createsuperuser"

create-financial-quarters:
	$(CMD) -f $(COMPOSEFILE) run --rm web sh -c "python manage.py create_financial_quarters 2021 2022 2023 2024 2025 2026 2027 2028"

clean:
	provision/clean_and_repopulate_database.sh

test-docker:
	$(CMD) -f $(COMPOSEFILE) run --rm web sh -c "python manage.py test"

test-fail-docker:
	$(CMD) -f $(COMPOSEFILE) run --rm web sh -c "python manage.py test --failfast"

test-fail-pdb-docker:
	$(CMD) -f $(COMPOSEFILE) run --rm web sh -c "python manage.py test --failfast --pdb"

test-api-docker:
	$(CMD) run --rm web sh -c 'python manage.py test --pattern="test_api.py"'
