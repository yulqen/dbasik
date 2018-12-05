import os

from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.urls import reverse_lazy
from django.views.generic import FormView

from excelparser.forms import ProcessPopulatedTemplateForm
from excelparser.helpers.parser import ParsedSpreadsheet


class ProcessPopulatedTemplate(FormView):
    form_class = ProcessPopulatedTemplateForm
    template_name = "excelparser/process_populated_template.html"

    def get_initial(self):
        return {'return_obj': self.kwargs['return_id']}

    def get_success_url(self):
        return str(reverse_lazy("returns:return_data", args=[self.kwargs['return_id']]))

    def form_valid(self, form):
        uploaded_file: UploadedFile = self.request.FILES['source_file']
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', uploaded_file.name)
        path = default_storage.save(save_path, uploaded_file)
        project = form.cleaned_data['return_obj'].project
        return_obj = form.cleaned_data['return_obj']
        datamap = form.cleaned_data['datamap']
        parsed_spreadsheet = ParsedSpreadsheet(path, project, return_obj, datamap)
        parsed_spreadsheet.process()
        return HttpResponseRedirect(self.get_success_url())
