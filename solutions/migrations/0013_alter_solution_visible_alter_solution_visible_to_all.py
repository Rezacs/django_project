# Generated by Django 4.2.7 on 2023-12-14 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0012_solution_visible_solution_visible_to_all_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='solution',
            name='visible_to_all',
            field=models.BooleanField(default=True),
        ),
    ]
