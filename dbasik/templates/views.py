import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, DetailView, ListView, UpdateView

from dbasik.templates.forms import TemplateCreateForm
from dbasik.templates.models import Template, TemplateDataLine


class TemplateList(LoginRequiredMixin, ListView):
    model = Template


class TemplateDetail(LoginRequiredMixin, DetailView):
    model = Template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cells = [{"A1": "Col A Key 1"}]
        parsed_template = [{"Test Sheet": cells}]
        context.update({"submitted_template": parsed_template})
        return context


class TemplateDelete(LoginRequiredMixin, DeleteView):
    model = Template
    success_url = reverse_lazy("templates:list")

    def get(self, request, *args, **kwargs):
        source_file = Template.objects.get(slug=kwargs["slug"]).source_file.url
        os.remove(source_file)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class TemplateUpdate(LoginRequiredMixin, UpdateView):
    model = Template
    form_class = TemplateCreateForm
    template_name_suffix = "_update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = Template.objects.all()
        context["existing_objects"] = existing_objects
        return context


@login_required
def template_create(request):
    """Create a new template CRUD function."""

    if request.method == "POST":
        form = TemplateCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("templates:list"))
        else:
            messages.error(
                request, "You can only upload a macro-enabled Excel file here (.xlsm). "
            )
            form = TemplateCreateForm()
    else:
        form = TemplateCreateForm()

    return render(request, "templates/template_create.html", {"form": form})
