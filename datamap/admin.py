from django.contrib import admin

from . models import Datamap, DatamapLine, PortfolioFamily

admin.site.register(Datamap)
admin.site.register(DatamapLine)
admin.site.register(PortfolioFamily)
