# Generated by Django 4.2.7 on 2023-12-19 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_site_slug_alter_site_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='secondry_sites',
            field=models.ManyToManyField(blank=True, null=True, related_name='secondry_sites', to='users.site'),
        ),
    ]