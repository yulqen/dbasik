from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from excelparser.forms import ProcessPopulatedTemplateForm


class ProcessPopulatedTemplate(FormView):
    form_class = ProcessPopulatedTemplateForm
    # TODO - fix this link
    success_url = reverse_lazy("dashboard")
    template_name = "excelparser/process_populated_template.html"
