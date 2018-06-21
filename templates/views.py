from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from templates.forms import TemplateCreateForm


def template_create(request):
    """Create a new template CRUD function."""

    if request.method == "POST":
        form = TemplateCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/datamaps')
    else:
        form = TemplateCreateForm()

    return render(request, "templates/template_create.html", {"form": form})
