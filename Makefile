COMPOSEFILE="docker-compose.yml"

clean-rebuild-and-run:
	docker-compose -f $(COMPOSEFILE) down && docker-compose -f $(COMPOSEFILE) up --build && docker-compose -f $(COMPOSEFILE) run app sh -c "python manage.py creat_financial_quarters"

createsuperuser:
	docker-compose -f $(COMPOSEFILE) run --rm app sh -c "python manage.py createsuperuser"

create-financial-quarters:
	docker-compose -f $(COMPOSEFILE) run --rm app sh -c "python manage.py create_financial_quarters 2021 2022 2023 2024 2025 2026 2027 2028"

clean:
	provision/clean_and_repopulate_database.sh

test:
	docker-compose -f docker-compose.yml run --rm app sh -c "python manage.py test"

test-fail:
	docker-compose -f docker-compose.yml run --rm app sh -c "python manage.py test --failfast"

test-fail-pdb:
	docker-compose -f docker-compose.yml run --rm app sh -c "python manage.py test --failfast --pdb"
