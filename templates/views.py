from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DeleteView, UpdateView, DetailView

from templates.forms import TemplateCreateForm
from templates.models import Template


class TemplateList(ListView):
    model = Template


class TemplateDetail(DetailView):
    model = Template


class TemplateDelete(DeleteView):
    model = Template
    success_url = reverse_lazy("templates:list")


class TemplateUpdate(UpdateView):
    model = Template
    form_class = TemplateCreateForm
    template_name_suffix = "_update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = Template.objects.all()
        context['existing_objects'] = existing_objects
        return context


def template_create(request):
    """Create a new template CRUD function."""

    if request.method == "POST":
        form = TemplateCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/templates')
        else:
            messages.error(
                request,
                "You can only upload a macro-enabled Excel file here (.xlsm). ")
            form = TemplateCreateForm()
    else:
        form = TemplateCreateForm()

    return render(request, "templates/template_create.html", {"form": form})


