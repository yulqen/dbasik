from django.core.management.base import BaseCommand, CommandError

from register.models import FinancialQuarter


class Command(BaseCommand):
    help = "Sets up a sensible range of Financial Quarters in the database"

    def add_arguments(self, parser):
        parser.add_argument('year', nargs='+', type=int)

    def handle(self, *args, **options):
        for opt in options['year']:
            FinancialQuarter.objects.create(quarter=1, year=opt)
            FinancialQuarter.objects.create(quarter=2, year=opt)
            FinancialQuarter.objects.create(quarter=3, year=opt)
            FinancialQuarter.objects.create(quarter=4, year=opt)
            self.stdout.write(self.style.SUCCESS(f"Created FinancialQuarter objects for the years: {opt}"))