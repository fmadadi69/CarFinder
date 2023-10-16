from django.db import models


# Create your models here.

class ScrapingReport(models.Model):
    report_date = models.DateTimeField()
    counts = models.IntegerField(default=0)
    last_retrieve_car = models.TextField()


class Car(models.Model):
    # scraping_report = models.ForeignKey(ScrapingReport, on_delete=models.CASCADE)
    make = models.CharField(max_length=100)
    mileage = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    location = models.CharField(max_length=250)
    price = models.CharField(max_length=100)
