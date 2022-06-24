from datetime import date

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField

from users.models import DfTGroup
from users.models import Employee
from users.models import Organisation


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

class FinancialQuarter(AppModel):
    quarter = models.IntegerField()
    year = models.IntegerField()
    start_date = models.DateField(blank=True, null=True, unique=True)
    end_date = models.DateField(blank=True, null=True)
    label = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.label

    class Meta:
        ordering = ['start_date']


@receiver(post_save, sender=FinancialQuarter)
def calculate_start_end_date_receiver(sender, instance, created, **kwargs):
    if created:
        if instance.quarter == 1:
            instance.start_date = date(instance.year, 4, 1)
            instance.end_date = date(instance.year, 6, 30)
            instance.label = f"Q{instance.quarter} {instance.year}"
        elif instance.quarter == 2:
            instance.start_date = date(instance.year, 7, 1)
            instance.end_date = date(instance.year, 9, 30)
            instance.label = f"Q{instance.quarter} {instance.year}"
        elif instance.quarter == 3:
            instance.start_date = date(instance.year, 10, 1)
            instance.end_date = date(instance.year, 12, 31)
            instance.label = f"Q{instance.quarter} {instance.year}"
        elif instance.quarter == 4:
            instance.start_date = date(instance.year + 1, 1, 1)
            instance.end_date = date(instance.year + 1, 3, 31)
            instance.label = f"Q{instance.quarter} {instance.year}"
        instance.save()


class ProjectType(AppModel):
    name = models.CharField(max_length=50, blank=False, unique=True)
    slug = AutoSlugField(populate_from=['name'])
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('register:projecttype_detail', args=[str(self.slug)])

    def __str__(self):
        return self.name


class Tier(AppModel):
    name = models.CharField(max_length=25, blank=False)
    slug = AutoSlugField(populate_from=['name'])
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('register:tier_list')

    def __str__(self):
        return self.name


class ProjectStage(AppModel):
    name = models.CharField(max_length=100, blank=False)
    slug = AutoSlugField(populate_from=['name'])
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('register:projectstage_list')

    def __str__(self):
        return self.name


class StrategicAlignment(AppModel):
    name = models.CharField(max_length=100, blank=False)
    slug = AutoSlugField(populate_from=['name'])
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('register:strategicalignment_list')

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


# pared-down class for prototype using existing objects

class Project(AppModel):
    name = models.CharField(max_length=255, blank=False)
    slug = AutoSlugField(populate_from=['name'])
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
    project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE, null=True)
    stage = models.ForeignKey(ProjectStage, on_delete=models.CASCADE, null=True)
    abbreviation = models.CharField(max_length=20, null=False, blank=False)
    dft_group = models.ForeignKey(DfTGroup, on_delete=models.CASCADE, null=False, blank=False)
    gmpp = models.BooleanField(default=False, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('register:project_list')

    def __str__(self):
        return self.name


#class Project(AppModel):
#    name = models.CharField(max_length=255, blank=False)
#    dependencies = models.ManyToManyField("Project", blank=True)
#    mandate = models.OneToOneField(Mandate, on_delete=models.CASCADE)
#    portfolio_initialisation = models.OneToOneField(
#        PortfolioInitialisation, on_delete=models.CASCADE, related_name="project_portfolio_initialisation"
#    )
#    mandate_active = models.BooleanField(default=False)
#    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
#    project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE, null=True)
#    stage = models.ForeignKey(ProjectStage, on_delete=models.CASCADE, null=True)
#    dft_group = models.ForeignKey(DfTGroup, on_delete=models.CASCADE, null=True)
#    sro = models.ForeignKey(
#        Employee,
#        on_delete=models.CASCADE,
#        blank=True,
#        null=True,
#        related_name="project_sro",
#    )
#    director = models.ForeignKey(
#        Employee,
#        on_delete=models.CASCADE,
#        blank=True,
#        null=True,
#        related_name="project_director",
#    )
#    agency_delivery_partner = models.ForeignKey(
#        Organisation, on_delete=models.CASCADE, blank=True, null=True
#    )
#    start_date = models.DateField(blank=True, null=True)
#    planned_end_date = models.DateField(blank=True, null=True)
#    baseline_wlc = models.FloatField(blank=True, null=True)
#
#    def __str__(self):
#        return " | ".join([self.name, self.tier])
