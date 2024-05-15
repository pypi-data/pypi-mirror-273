from django.contrib import admin
from .models import ExtraFile

@admin.register(ExtraFile)
class ExtraFileAdmin(admin.ModelAdmin):
    list_display = ('circuit', 'name')
