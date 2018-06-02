from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from register.models import Tier

import uuid


class Datamap(models.Model):
    """A datamap in the system."""

    name = models.CharField(max_length=25)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=50, blank=True, default=uuid.uuid1)

    class Meta:
        unique_together = ("name", "tier")

    def get_absolute_url(self):
        return reverse('datamaps:datamap_detail', args=[str(self.slug)])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify("-".join([self.name, self.tier.name]))
        super().save(*args, **kwargs)


class DatamapLine(models.Model):
    """A single line in the datamap."""
    datamap = models.ForeignKey("Datamap", on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    sheet = models.CharField(max_length=50)
    cell_ref = models.CharField(max_length=10)

    class Meta:
        unique_together = ("datamap", "sheet", "cell_ref")

    def __str__(self):
        return f"{self.key} for {self.datamap}"
