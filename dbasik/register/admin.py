from django.contrib import admin
from django.contrib.admin import ModelAdmin

# from register.models import Classification
# from register.models import Constraint
# from register.models import Deliverable
from register.models import FinancialQuarter
# from register.models import Mandate
# from register.models import Milestone
from register.models import Objective
from register.models import Organisation
# from register.models import PortfolioInitialisation
from register.models import Project
from register.models import ProjectStage
from register.models import ProjectType
# from register.models import RAGColour
# from register.models import RiskRPA
# from register.models import StrategicAlignment
# from register.models import StrategicOutcome
from register.models import Tier
from users.models import DfTDivision
from users.models import DfTGroup
# from users.models import Employee


class FinancialQuarterAdmin(ModelAdmin):
     list_display = ('label', 'start_date', 'end_date')

admin.site.register(FinancialQuarter, FinancialQuarterAdmin)
admin.site.register(Project)
admin.site.register(Tier)
admin.site.register(ProjectType)
admin.site.register(ProjectStage)
# admin.site.register(StrategicAlignment)
admin.site.register(Organisation)
admin.site.register(Objective)
# admin.site.register(StrategicOutcome)
# admin.site.register(Deliverable)
# admin.site.register(Constraint)
# admin.site.register(RAGColour)
# admin.site.register(RiskRPA)
# admin.site.register(Mandate)
# admin.site.register(Classification)
# admin.site.register(Milestone)
# admin.site.register(PortfolioInitialisation)

admin.site.register(DfTGroup)
admin.site.register(DfTDivision)
# admin.site.register(Employee)


