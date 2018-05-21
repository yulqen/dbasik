from django.db import models
from django.utils.text import slugify

import uuid


class Datamap(models.Model):
    """A datamap in the system."""

    name = models.CharField(max_length=50)
    portfolio_family = models.ForeignKey(
        "PortfolioFamily", on_delete=models.CASCADE, related_name="datamaps"
    )
    active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=50, blank=True, default=uuid.uuid1)

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("slug", "portfolio_family")



class DatamapLine(models.Model):
    """A single line in the datamap."""
    datamap = models.ForeignKey("Datamap", on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    sheet = models.CharField(max_length=50)
    cell_ref = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.key} for {self.datamap}"


class PortfolioFamily(models.Model):
    """Tier 1, Tier 2, etc"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
