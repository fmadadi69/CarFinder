# Generated by Django 4.2.5 on 2023-10-18 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=100)),
                ('mileage', models.CharField(max_length=100)),
                ('condition', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=250)),
                ('price', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CarPrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=100)),
                ('mileage', models.CharField(max_length=100)),
                ('predicted_price', models.CharField(max_length=100)),
                ('prediction_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ScrapingReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_date', models.DateTimeField()),
                ('counts', models.IntegerField(default=0)),
                ('last_retrieve_car', models.TextField()),
            ],
        ),
    ]
