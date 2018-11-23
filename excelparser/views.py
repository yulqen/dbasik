import datetime

from django.urls import reverse_lazy
from django.views.generic import FormView

from excelparser.forms import ProcessPopulatedTemplateForm
from excelparser.helpers.financial_quarter import check_date_in_quarter
from register.models import FinancialQuarter


class ProcessPopulatedTemplate(FormView):
    form_class = ProcessPopulatedTemplateForm
    # TODO - fix this link
    success_url = reverse_lazy("dashboard")
    template_name = "excelparser/process_populated_template.html"

    def get_initial(self):
        today = datetime.date.today()
        for q in FinancialQuarter.objects.all():
            if check_date_in_quarter(today, q):
                return {'financial_quarter': q}
        return None
