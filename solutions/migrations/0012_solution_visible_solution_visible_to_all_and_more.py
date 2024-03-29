# Generated by Django 4.2.7 on 2023-12-14 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0011_solution_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='visible',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AddField(
            model_name='solution',
            name='visible_to_all',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.DeleteModel(
            name='SitezSolution',
        ),
    ]
