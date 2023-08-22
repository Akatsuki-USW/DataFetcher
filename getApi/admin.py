from django.contrib import admin
from getApi.models import Congestion,Location,DailyCongestionStatistic,WeeklyCongestionStatistic

admin.site.register(Congestion)
admin.site.register(Location)
admin.site.register(DailyCongestionStatistic)
admin.site.register(WeeklyCongestionStatistic)


# Register your models here.
