from django.db import models
from datetime import date
from users.models import Employee, DfTGroup, Organisation

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
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name


class Tier(AppModel):
    name = models.CharField(max_length=50, blank=False)
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
    known_constraints = models.ManyToManyField(Constraint, null=True)
    internal_organisations_affected = models.ManyToManyField(DfTGroup, null=True)
    external_organisations_affected = models.ManyToManyField(Organisation, null=True)
    critical_success_factor = models.TextField(blank=True)
    objectives = models.ManyToManyField(Objective, null=True)
    major_deliverables = models.ManyToManyField(Deliverable, null=True)
    strategic_outcomes = models.ManyToManyField(StrategicOutcome, null=True)


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
    key_milestones = models.ManyToManyField(Milestone)
    sobc_approval = models.DateField(blank=True, null=True)
    obc_approval = models.DateField(blank=True, null=True)
    fbc_approval = models.DateField(blank=True, null=True)
    start_of_operations_at_initialisation = models.DateField(blank=True, null=True)
    start_of_construction_build_at_initialisation = models.DateField(
        blank=True, null=True
    )
    initial_project_assurance_milestones = models.ManyToManyField(Milestone)


class Project(AppModel):
    name = models.CharField(max_length=255, blank=False)
    dependencies = models.ManyToManyField("Project")
    mandate = models.OneToOneField(Mandate, on_delete=models.CASCADE)
    portfolio_initialisation = models.OneToOneField(
        PortfolioInitialisation, on_delete=models.CASCADE
    )
    mandate_active = models.BooleanField(default=False)
    portfolio_initialisation = models.ForeignKey(
        PortfolioInitialisation, on_delete=models.CASCADE, null=True
    )
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
