import datetime

from dbasik.register.models import FinancialQuarter


def check_date_in_quarter(
    date: datetime.date, financial_quarter: FinancialQuarter
) -> bool:
    if financial_quarter.start_date < date < financial_quarter.end_date:
        return True
    else:
        return False
