# Generated by Django 4.0.1 on 2022-01-14 10:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('opensea', '0004_collection_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='updated',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
