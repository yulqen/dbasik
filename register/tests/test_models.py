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

    @unittest.skip("Not ready for this yet")
    def test_series_financial_objects(self):
        fq1 = FinancialQuarter(quarter=1, year=2010)
        fq2 = FinancialQuarter(quarter=2, year=2010)
        fq1.save()
        fq2.save()
        self.assertTrue(fq2 > fq2)
