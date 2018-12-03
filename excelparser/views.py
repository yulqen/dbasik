from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from excelparser.forms import ProcessPopulatedTemplateForm


class ProcessPopulatedTemplate(FormView):
    form_class = ProcessPopulatedTemplateForm
    # TODO - fix this link
    template_name = "excelparser/process_populated_template.html"

    def get_initial(self):
        return {'return_obj': self.kwargs['return_id']}

    def get_success_url(self):
        return str(reverse_lazy("returns:return_data", args=[self.kwargs['return_id']]))

    def form_valid(self, form):
        print("Here is where we process the spreadsheet!")
        # this is a form to handle a single form - we will do zip files elsewhere
        print(self.request.FILES['source_file'])
        return HttpResponseRedirect(self.get_success_url())
