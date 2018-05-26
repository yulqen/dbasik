from django.contrib import admin
from register.models import (Project, Tier, ProjectPhase, ProjectType,
                             AgencyDeliveryPartner, ProjectStage, StrategicAlignment,
                             Organisation, Objective, StrategicOutcome, Deliverable,
                             Constraint, RAGColour, RiskRPA, Mandate, Classification,
                             Milestone, PortfolioInitialisation)

from users.models import DfTGroup, Division, Employee

admin.site.register(Project)
admin.site.register(Tier)
admin.site.register(ProjectPhase)
admin.site.register(ProjectType)
admin.site.register(AgencyDeliveryPartner)
admin.site.register(ProjectStage)
admin.site.register(StrategicAlignment)
admin.site.register(Organisation)
admin.site.register(Objective)
admin.site.register(StrategicOutcome)
admin.site.register(Deliverable)
admin.site.register(Constraint)
admin.site.register(RAGColour)
admin.site.register(RiskRPA)
admin.site.register(Mandate)
admin.site.register(Classification)
admin.site.register(Milestone)
admin.site.register(PortfolioInitialisation)

admin.site.register(DfTGroup)
admin.site.register(Division)
admin.site.register(Employee)
