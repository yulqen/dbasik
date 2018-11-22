import unittest
from datetime import date

from django.test import TestCase

from register.models import FinancialQuarter


class ModelTests(TestCase):
    def test_financial_quarter_model(self):
        """
        We need to create FinancialQuarter model objects using a Manager
        to ensure we get correct attributes regarding start/end dates, etc.
        Another way to do this would be using Signals perhaps.
        :return:
        :rtype: None
        """
        fq = FinancialQuarter(quarter=1, year=2010)
        fq.save()
        self.assertEqual(fq.end_date, date(2010, 6, 30))

