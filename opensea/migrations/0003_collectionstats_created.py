# Generated by Django 4.0.1 on 2022-01-14 09:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('opensea', '0002_remove_collection_average_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectionstats',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
