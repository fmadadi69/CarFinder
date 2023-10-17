from django.contrib import admin

# Register your models here.
from .models import ScrapingReport, Car


def insert_cars_into_database(admin, request, queryset):
    from django.core import management
    management.call_command('insert_data')


insert_cars_into_database.short_description = "Insert cars into database"


class CarAdmin(admin.ModelAdmin):
    actions = [insert_cars_into_database]
    list_display = ['make', 'year', 'mileage', 'condition', 'location', 'price']


class ScrapingReportAdmin(admin.ModelAdmin):
    list_display = ['report_date', 'counts', 'last_retrieve_car']


admin.site.register(Car, CarAdmin)
admin.site.register(ScrapingReport, ScrapingReportAdmin)



