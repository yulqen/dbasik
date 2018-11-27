import datetime

from django.urls import reverse_lazy
from django.views.generic import FormView

from excelparser.forms import ProcessPopulatedTemplateForm
from returns.models import Return


class ProcessPopulatedTemplate(FormView):
    form_class = ProcessPopulatedTemplateForm
    # TODO - fix this link
    success_url = reverse_lazy("dashboard")
    template_name = "excelparser/process_populated_template.html"

    def get_initial(self):
        return {'return_obj': self.kwargs['return_id']}
