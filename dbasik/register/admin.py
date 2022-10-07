from django.contrib import admin
from django.contrib.admin import ModelAdmin

# from dbasik.register.models import Classification
# from dbasik.register.models import Constraint
# from dbasik.register.models import Deliverable
from dbasik.register.models import FinancialQuarter

# from dbasik.register.models import Mandate
# from dbasik.register.models import Milestone
from dbasik.register.models import Objective
from dbasik.register.models import Organisation

# from dbasik.register.models import PortfolioInitialisation
from dbasik.register.models import Project
from dbasik.register.models import ProjectStage
from dbasik.register.models import ProjectType

# from dbasik.register.models import RAGColour
# from dbasik.register.models import RiskRPA
# from dbasik.register.models import StrategicAlignment
# from dbasik.register.models import StrategicOutcome
from dbasik.register.models import Tier
from dbasik.users.models import DfTDivision
from dbasik.users.models import DfTGroup

# from users.models import Employee


class FinancialQuarterAdmin(ModelAdmin):
    list_display = ("label", "start_date", "end_date")


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
