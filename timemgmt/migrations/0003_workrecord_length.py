# Generated by Django 4.2.7 on 2024-01-21 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timemgmt', '0002_workrecord_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='workrecord',
            name='length',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
