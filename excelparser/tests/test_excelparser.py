import datetime

from django.test import TestCase

from excelparser.helpers.financial_year import Quarter, FinancialYear


class FinancialYearQuarterTests(TestCase):

    def setUp(self):
        self.fy = FinancialYear(2010)

    def test_create_fy_quarter(self):
        q = Quarter(2010, 3)
        self.assertEqual(q.fy, self.fy)
        self.assertEqual(q.start_date, datetime.date(2010, 10, 1))

    def test_incorrect_quarter(self):
        with self.assertRaisesMessage(ValueError, "A quarter must be either 1, 2, 3 or 4"):
            q = Quarter(2010, 5)


class FinancialYearTests(TestCase):

    def setUp(self):
        self.fy = FinancialYear(2010)

    def test_financial_year_creation(self):
        self.assertEqual(self.fy.year, 2010)
        self.assertEqual(self.fy.end_date, datetime.date(2011, 3, 31))

    def test_financial_year_objects_are_equal(self):
        fy1 = FinancialYear(2010)
        fy2 = FinancialYear(2010)
        self.assertEqual(fy1, fy2)

    def test_compare_financial_year_with_different_object(self):
        with self.assertRaisesMessage(ValueError,
                                      "Can only compare FinancialYear object with another FinancialYear object"):
            self.fy == 1
        with self.assertRaisesMessage(ValueError,
                                      "Can only compare FinancialYear object with another FinancialYear object"):
            self.fy == "2010"

    def test_financial_quarter_creation(self):
        q = Quarter(2010, 1)
        self.assertEqual(q.fy, self.fy)

    def test_correct_financialyear_creation(self):
        with self.assertRaisesMessage(ValueError, "A year must be an integer between 1950 and 2100"):
            fy = FinancialYear(20)
        with self.assertRaisesMessage(ValueError, "A year must be an integer between 1950 and 2100"):
            fy = FinancialYear("2012")
