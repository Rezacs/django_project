# Generated by Django 4.2.7 on 2023-12-14 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_site_slug_alter_site_name'),
        ('solutions', '0008_sitesolution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesolution',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.site'),
        ),
    ]
