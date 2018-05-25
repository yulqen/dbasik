from django.contrib import admin
from register.models import Project, Tier, ProjectPhase
from users.models import DfTGroup, Division, Employee

admin.site.register(Project)
admin.site.register(Tier)
admin.site.register(ProjectPhase)

admin.site.register(DfTGroup)
admin.site.register(Division)
admin.site.register(Employee)
