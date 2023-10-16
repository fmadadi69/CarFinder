from django.contrib import admin

# Register your models here.
from .models import ScrapingReport, Car


def insert_cars_into_database(admin, request, queryset):
    print("in insert_cars_into_database")
    from django.core import management
    management.call_command('insert_data')


insert_cars_into_database.short_description = "Insert cars into database"


class CarAdmin(admin.ModelAdmin):
    actions = [insert_cars_into_database]
    print('In Caradmin')


admin.site.register(Car, CarAdmin)



