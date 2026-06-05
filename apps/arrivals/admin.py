from django.contrib import admin
from .models import Arrival


@admin.register(Arrival)
class ArrivalAdmin(admin.ModelAdmin):
    list_display = ['id', 'timestamp', 'latitude', 'longitude', 'device_id']
    list_filter = ['device_id']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
