from django.db import models
from django.urls import reverse

from django_extensions.db.fields import AutoSlugField


class Template(models.Model):
    """A template used to collect data from a user."""
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    source_file = models.FileField(upload_to="uploaded_templates/")
    slug = AutoSlugField(populate_from=['name'])

    def get_absolute_url(self):
        return reverse('templates:template_detail', args=[str(self.slug)])

    def __str__(self):
        return f"Template({self.name})"


class TemplateDataLine(models.Model):
    """When data is pulled from a blank template, it is put in here."""
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name="data")
    sheet = models.CharField(max_length=255, blank=False)
    cellref = models.CharField(max_length=10, blank=False)
    value = models.CharField(max_length=255, blank=True, null=True)


