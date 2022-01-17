# Generated by Django 4.0.1 on 2022-01-14 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField()),
                ('editors', models.JSONField(default=list)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=100)),
                ('one_day_volume', models.FloatField(blank=True, default=0.0)),
                ('one_day_change', models.FloatField(blank=True, default=0.0)),
                ('one_day_sales', models.FloatField(blank=True, default=0.0)),
                ('one_day_average_price', models.FloatField(blank=True, default=0.0)),
                ('seven_day_volume', models.FloatField(blank=True, default=0.0)),
                ('seven_day_change', models.FloatField(blank=True, default=0.0)),
                ('seven_day_sales', models.FloatField(blank=True, default=0.0)),
                ('seven_day_average_price', models.FloatField(blank=True, default=0.0)),
                ('thirty_day_volume', models.FloatField(blank=True, default=0.0)),
                ('thirty_day_change', models.FloatField(blank=True, default=0.0)),
                ('thirty_day_sales', models.FloatField(blank=True, default=0.0)),
                ('thirty_day_average_price', models.FloatField(blank=True, default=0.0)),
                ('total_volume', models.FloatField(blank=True, default=0.0)),
                ('total_sales', models.FloatField(blank=True, default=0.0)),
                ('total_supply', models.FloatField(blank=True, default=0.0)),
                ('count', models.FloatField(blank=True, default=0.0)),
                ('num_owners', models.FloatField(blank=True, default=0.0)),
                ('average_price', models.FloatField(blank=True, default=0.0)),
                ('num_reports', models.FloatField(blank=True, default=0.0)),
                ('market_cap', models.FloatField(blank=True, default=0.0)),
                ('floor_price', models.FloatField(blank=True, default=0.0)),
            ],
            options={
                'verbose_name': 'Collection',
                'verbose_name_plural': 'Collections',
            },
        ),
    ]
