# Generated by Django 4.2.7 on 2023-12-14 20:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0006_rename_ticket_number_ticket_number'),
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('satisfy', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('opinion', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.ticket')),
            ],
        ),
    ]
