# Generated by Django 4.2.7 on 2023-12-14 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0013_alter_solution_visible_alter_solution_visible_to_all'),
        ('ticket', '0006_rename_ticket_number_ticket_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='solution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='solutions.solution'),
        ),
    ]
