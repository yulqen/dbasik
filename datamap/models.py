from django.db import models


class Datamap(models.Model):
    """A datamap in the system."""

    name = models.CharField(max_length=50)
    portfolio_family = models.ForeignKey(
        'PortfolioFamily', on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class DatamapLine(models.Model):
    """A single line in the datamap."""
    datamap = models.ForeignKey('Datamap', on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    sheet = models.CharField(max_length=50)
    cell_ref = models.CharField(max_length=10)

    def __str__(self):
        return "{0} for {1}".format(self.key, self.datamap)


class PortfolioFamily(models.Model):
    """Tier 1, Tier 2, etc"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
