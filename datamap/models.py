from django.db import models
from django.utils.text import slugify


def _slugify(self):
    return slugify(self.name)


class Datamap(models.Model):
    """A datamap in the system."""

    name = models.CharField(max_length=50)
    portfolio_family = models.ForeignKey(
        "PortfolioFamily", on_delete=models.CASCADE, related_name="datamaps"
    )
    active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=50, blank=True, default=_slugify)

    class Meta:
        unique_together = ("slug", "portfolio_family")

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


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
