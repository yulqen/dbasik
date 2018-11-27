from django.db import models

from datamap.models import Datamap
from datamap.models import DatamapLine
from register.models import FinancialQuarter
from register.models import Project


class Return(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="return_projects"
    )
    financial_quarter = models.ForeignKey(
        FinancialQuarter,
        on_delete=models.CASCADE,
        related_name="return_financial_quarters",
    )

    class Meta:
        unique_together = ['project', 'financial_quarter']

    def __str__(self):
        return f"Return for {self.project} for {self.financial_quarter}"


class ReturnItem(models.Model):
    """
    A model in which to store parsed template data. The value should
    be stored as the appropriate type, therefore the form should use
    a routine to select appropriately.
    """

    parent = models.ForeignKey(Return, on_delete=models.CASCADE)
    datamapline = models.ForeignKey(
        DatamapLine,
        on_delete=models.CASCADE,
        null=True,
        related_name="return_datamaplines",
    )
    value_str = models.CharField(blank=True, max_length=255, default="")
    value_int = models.IntegerField(blank=True, null=True)
    value_float = models.DecimalField(
        blank=True, max_digits=9, decimal_places=2, null=True
    )
    value_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.datamapline.key} for {self.parent}"
