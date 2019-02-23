from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, UpdateView

from templates.forms import TemplateCreateForm
from templates.models import Template


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


class TemplateUpdate(LoginRequiredMixin, UpdateView):
    model = Template
    form_class = TemplateCreateForm
    template_name_suffix = "_update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_objects = Template.objects.all()
        context['existing_objects'] = existing_objects
        return context


@login_required
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
