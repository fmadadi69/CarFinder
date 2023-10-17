from django.contrib import admin
from django.http import HttpResponseRedirect

# Register your models here.
from .models import ScrapingReport, Car
from django.urls import path


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    # actions = [insert_cars_into_database]
    list_display = ['make', 'year', 'mileage', 'condition', 'location', 'price']
    change_list_template = 'admin/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('insert_cars_into_database/', self.insert_cars_into_database, name="insert_cars_into_database"),
        ]
        return custom_urls + urls

    def insert_cars_into_database(self, request):
        from django.core import management
        management.call_command('insert_data')
        self.message_user(request, 'Cars inserted successfully.')
        # return HttpResponseRedirect(request.path)


class ScrapingReportAdmin(admin.ModelAdmin):
    list_display = ['report_date', 'counts', 'last_retrieve_car']


# admin.site.register(Car, CarAdmin)
admin.site.register(ScrapingReport, ScrapingReportAdmin)
