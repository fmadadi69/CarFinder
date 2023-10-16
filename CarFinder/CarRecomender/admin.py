from django.contrib import admin

# Register your models here.
from .models import ScrapingReport, Cars


class ScrapingReportAdmin(admin.ModelAdmin):
    actions = []
    model = ScrapingReport


admin.site.register(ScrapingReport, ScrapingReportAdmin)
