from django.db import models
from datetime import date
from users.models import Employee, DfTGroup

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


class Organisation(AppModel):
    name = models.CharField(max_length=50)
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
    background = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Deliverable(AppModel):
    name = models.CharField(max_length=50)
    background = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Constraint(AppModel):
    name = models.CharField(max_length=50)
    background = models.TextField(blank=True)

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
    internal_organisation_affected1 = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_internal_org_affected1",
    )
    internal_organisation_affected2 = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_internal_org_affected2",
    )
    internal_organisation_affected3 = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_internal_org_affected3",
    )
    internal_organisation_affected4 = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_internal_org_affected4",
    )
    internal_organisation_affected5 = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_internal_org_affected5",
    )
    external_organisation_affected1 = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_external_org_affected1",
    )
    external_organisation_affected2 = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_external_org_affected2",
    )
    external_organisation_affected3 = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_external_org_affected3",
    )
    external_organisation_affected4 = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_external_org_affected4",
    )
    external_organisation_affected5 = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_external_org_affected5",
    )
    critIcal_success_factor = models.TextField(blank=True)
    objective1 = models.ForeignKey(
        Objective,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_objective_1",
    )
    objective2 = models.ForeignKey(
        Objective,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_objective_2",
    )
    objective3 = models.ForeignKey(
        Objective,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_objective_3",
    )
    objective4 = models.ForeignKey(
        Objective,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_objective_4",
    )
    objective5 = models.ForeignKey(
        Objective,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_objective_5",
    )
    strategic_outcome1 = models.ForeignKey(
        StrategicOutcome,
        on_delete=models.CASCADE,
        null=True,
        related_name="portfolio_strat_outcome1",
    )
    strategic_outcome2 = models.ForeignKey(
        StrategicOutcome,
        on_delete=models.CASCADE,
        null=True,
        related_name="portfolio_strat_outcome2",
    )
    strategic_outcome3 = models.ForeignKey(
        StrategicOutcome,
        on_delete=models.CASCADE,
        null=True,
        related_name="portfolio_strat_outcome3",
    )
    strategic_outcome4 = models.ForeignKey(
        StrategicOutcome,
        on_delete=models.CASCADE,
        null=True,
        related_name="portfolio_strat_outcome4",
    )
    strategic_outcome5 = models.ForeignKey(
        StrategicOutcome,
        on_delete=models.CASCADE,
        null=True,
        related_name="portfolio_strat_outcome5",
    )
    deliverable1 = models.ForeignKey(Deliverable, on_delete=models.CASCADE, null=True, related_name="mandate_deliverable1")
    deliverable2 = models.ForeignKey(Deliverable, on_delete=models.CASCADE, null=True, related_name="mandate_deliverable2")
    deliverable3 = models.ForeignKey(Deliverable, on_delete=models.CASCADE, null=True, related_name="mandate_deliverable3")
    deliverable4 = models.ForeignKey(Deliverable, on_delete=models.CASCADE, null=True, related_name="mandate_deliverable4")
    deliverable5 = models.ForeignKey(Deliverable, on_delete=models.CASCADE, null=True, related_name="mandate_deliverable5")
    known_constraint1 = models.ForeignKey(
        Constraint,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_constraint1",
    )
    known_constraint2 = models.ForeignKey(
        Constraint,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_constraint2",
    )
    known_constraint3 = models.ForeignKey(
        Constraint,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_constraint3",
    )
    known_constraint4 = models.ForeignKey(
        Constraint,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_constraint4",
    )
    known_constraint5 = models.ForeignKey(
        Constraint,
        on_delete=models.CASCADE,
        null=True,
        related_name="mandate_constraint5",
    )
    key_risk1 = models.ForeignKey(
        RiskRPA, on_delete=models.CASCADE, null=True, related_name="mandate_key_risk1"
    )
    key_risk2 = models.ForeignKey(
        RiskRPA, on_delete=models.CASCADE, null=True, related_name="mandate_key_risk2"
    )
    key_risk3 = models.ForeignKey(
        RiskRPA, on_delete=models.CASCADE, null=True, related_name="mandate_key_risk3"
    )
    key_risk4 = models.ForeignKey(
        RiskRPA, on_delete=models.CASCADE, null=True, related_name="mandate_key_risk4"
    )
    key_risk5 = models.ForeignKey(
        RiskRPA, on_delete=models.CASCADE, null=True, related_name="mandate_key_risk5"
    )


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
    classification = models.ForeignKey(
        Classification, on_delete=models.CASCADE, null=True
    )
    risk_level = models.ForeignKey(RiskRPA, on_delete=models.CASCADE, null=True)
    project_methodology = models.TextField()
    group = models.ForeignKey(DfTGroup, on_delete=models.CASCADE, null=True)
    agency_delivery_partner = models.ForeignKey(
        AgencyDeliveryPartner, on_delete=models.CASCADE, blank=True
    )
    start_date = models.DateField(blank=True, null=True)
    planned_end_date = models.DateField(blank=True, null=True)
    milestone1 = models.ForeignKey(
        Milestone,
        on_delete=models.CASCADE,
        null=True,
        related_name="portfolio_init_milestone1",
    )
    milestone2 = models.ForeignKey(
        Milestone,
        on_delete=models.CASCADE,
        null=True,
        related_name="portfolio_init_milestone2",
    )
    milestone3 = models.ForeignKey(
        Milestone,
        on_delete=models.CASCADE,
        null=True,
        related_name="portfolio_init_milestone3",
    )
    strategic_outline_business_case_approval = models.DateField(blank=True, null=True)
    outline_business_case_approval = models.DateField(blank=True, null=True)
    full_business_case_approval = models.DateField(blank=True, null=True)
    start_of_construction_build = models.DateField(blank=True, null=True)
    start_of_operations = models.DateField(blank=True, null=True)
    initial_project_assurance_milestone1 = models.ForeignKey(
        Milestone,
        on_delete=models.CASCADE,
        null=True,
        related_name="portfolio_init_assurance_milestone1",
    )
    initial_project_assurance_milestone2 = models.ForeignKey(
        Milestone,
        on_delete=models.CASCADE,
        null=True,
        related_name="portfolio_init_assurance_milestone2",
    )
    initial_project_assurance_milestone3 = models.ForeignKey(
        Milestone,
        on_delete=models.CASCADE,
        null=True,
        related_name="portfolio_init_assurance_milestone3",
    )
    initial_project_assurance_milestone4 = models.ForeignKey(
        Milestone,
        on_delete=models.CASCADE,
        null=True,
        related_name="portfolio_init_assurance_milestone4",
    )
    initial_project_assurance_milestone5 = models.ForeignKey(
        Milestone,
        on_delete=models.CASCADE,
        null=True,
        related_name="portfolio_init_assurance_milestone5",
    )


class Project(AppModel):
    name = models.CharField(max_length=255, blank=False)
    mandate = models.ForeignKey(Mandate, on_delete=models.CASCADE, null=True)
    mandate_active = models.BooleanField(default=False)
    portfolio_initialisation = models.ForeignKey(
        PortfolioInitialisation, on_delete=models.CASCADE, null=True
    )
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
    dependency = models.ForeignKey(
        "Project", on_delete=models.CASCADE, blank=True, null=True
    )
    project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE, null=True)
    phase = models.ForeignKey(ProjectPhase, on_delete=models.CASCADE, null=True)
    stage = models.ForeignKey(ProjectStage, on_delete=models.CASCADE, null=True)
    dft_group = models.ForeignKey(DfTGroup, on_delete=models.CASCADE, null=True)
    sro = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True, related_name="project_sro")
    director = models.ForeignKey(
        Employee, on_delete=models.CASCADE, blank=True, null=True, related_name="project_director"
    )
    agency_delivery_partner = models.ForeignKey(
        AgencyDeliveryPartner, on_delete=models.CASCADE, blank=True, null=True
    )
    start_date = models.DateField(blank=True, null=True)
    planned_end_date = models.DateField(blank=True, null=True)
    baseline_wlc = models.FloatField(blank=True, null=True)

    def __str__(self):
        return " | ".join([self.name, self.tier])
