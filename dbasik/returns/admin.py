from django.contrib import admin

from dbasik.returns.models import ReturnItem, Return

admin.site.register(Return)
admin.site.register(ReturnItem)
