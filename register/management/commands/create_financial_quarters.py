from django.core.management.base import BaseCommand, CommandError
from excelparser.helpers.financial_year import FinancialYear

class Command(BaseCommand):
    help = "Sets up a sensible range of Financial Quarters in the database"

    def add_arguments(self, parser):
        parser.add_argument('first_quarter', nargs='+')