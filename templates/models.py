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
        return f"Template<{self.name}>"
