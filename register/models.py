from django.db import models
from users.models import Employee, DfTGroup


class AppQuerySet(models.QuerySet):
    pass


class AppManager(models.Manager):

    queryset_class = AppQuerySet

    def get_query(self):
        return self.queryset_class(self.model)


class AppModel(models.Model):
    objects = AppManager()

    class Meta:
        abstract = True


class ProjectType(AppModel):
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name


class AgencyDeliveryPartner(AppModel):
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name


class Tier(AppModel):
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ProjectPhase(AppModel):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ProjectStage(AppModel):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)


    def __str__(self):
        return self.name


class StrategicAlignment(AppModel):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Project(AppModel):
    name = models.CharField(max_length=255, blank=False)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
    dependency = models.ForeignKey("Project", on_delete=models.CASCADE, blank=True, null=True)
    project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE)
    phase = models.ForeignKey(ProjectPhase, on_delete=models.CASCADE)
    stage = models.ForeignKey(ProjectStage, on_delete=models.CASCADE)
    dft_group = models.ForeignKey(DfTGroup, on_delete=models.CASCADE)
    sro = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="sro_projects", blank=True)
    director = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="director_projects", blank=True)
    agency_delivery_partner = models.ForeignKey(AgencyDeliveryPartner, on_delete=models.CASCADE, blank=True)
    start_date = models.DateField(blank=True)
    planned_end_date = models.DateField(blank=True)
    baseline_wlc = models.FloatField(blank=True)

    def __str__(self):
        return self.name
