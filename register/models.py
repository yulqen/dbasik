from django.db import models
from datetime import date
from users.models import Employee, DfTGroup, Organisation

from django_extensions.db.fields import AutoSlugField
from django.urls import reverse

###############
# superclasses#
###############


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


##############
# app classes#
##############


class ProjectType(AppModel):
    name = models.CharField(max_length=50, blank=False, unique=True)
    slug = AutoSlugField(populate_from=['name'])
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('register:projecttype_detail', args=[str(self.slug)])

    def __str__(self):
        return self.name


class Tier(AppModel):
    name = models.CharField(max_length=50, blank=False)
    slug = AutoSlugField(populate_from=['name'])
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('register:tier_detail', args=[str(self.slug)])

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


class Objective(AppModel):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class StrategicOutcome(AppModel):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Deliverable(AppModel):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Constraint(AppModel):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class RAGColour(AppModel):
    colour = models.CharField(max_length=10)

    def __str__(self):
        return self.colour


class RiskRPA(AppModel):
    name = models.CharField(max_length=50)
    color = models.ForeignKey(RAGColour, on_delete=models.CASCADE, null=True)
    background = models.TextField(blank=True)

    def __str__(self):
        return " | ".join([self.name, self.colour])


class Mandate(AppModel):
    current_position = models.TextField(blank=True)
    known_constraints = models.ManyToManyField(Constraint)
    internal_organisations_affected = models.ManyToManyField(DfTGroup)
    external_organisations_affected = models.ManyToManyField(Organisation)
    critical_success_factor = models.TextField(blank=True)
    objectives = models.ManyToManyField(Objective)
    major_deliverables = models.ManyToManyField(Deliverable)
    strategic_outcomes = models.ManyToManyField(StrategicOutcome)


class Classification(AppModel):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Milestone(AppModel):
    name = models.CharField(max_length=50)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        d = date(self.date)
        return " | ".join([self.name, d])


class PortfolioInitialisation(AppModel):
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    portfolio_reference = models.CharField(max_length=5, blank=True)
    classification = models.ForeignKey(
        Classification, on_delete=models.CASCADE, null=True
    )
    rpa_rating = models.ForeignKey(RiskRPA, on_delete=models.CASCADE, null=True)
    project_methodology = models.TextField()
    start_date_at_initialisation = models.DateField(blank=True, null=True)
    planned_end_date_at_initialisation = models.DateField(blank=True, null=True)
    key_milestones = models.ManyToManyField(Milestone, related_name="pi_initial_milestones")
    sobc_approval = models.DateField(blank=True, null=True)
    obc_approval = models.DateField(blank=True, null=True)
    fbc_approval = models.DateField(blank=True, null=True)
    start_of_operations_at_initialisation = models.DateField(blank=True, null=True)
    start_of_construction_build_at_initialisation = models.DateField(
        blank=True, null=True
    )
    initial_project_assurance_milestones = models.ManyToManyField(Milestone, related_name="initial_milestones")


class Project(AppModel):
    name = models.CharField(max_length=255, blank=False)
    dependencies = models.ManyToManyField("Project", blank=True)
    mandate = models.OneToOneField(Mandate, on_delete=models.CASCADE)
    portfolio_initialisation = models.OneToOneField(
        PortfolioInitialisation, on_delete=models.CASCADE, related_name="project_portfolio_initialisation"
    )
    mandate_active = models.BooleanField(default=False)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
    project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE, null=True)
    stage = models.ForeignKey(ProjectStage, on_delete=models.CASCADE, null=True)
    dft_group = models.ForeignKey(DfTGroup, on_delete=models.CASCADE, null=True)
    sro = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="project_sro",
    )
    director = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="project_director",
    )
    agency_delivery_partner = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, blank=True, null=True
    )
    start_date = models.DateField(blank=True, null=True)
    planned_end_date = models.DateField(blank=True, null=True)
    baseline_wlc = models.FloatField(blank=True, null=True)

    def __str__(self):
        return " | ".join([self.name, self.tier])
