# Generated by Django 4.2.7 on 2023-12-14 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_site_slug_alter_site_name'),
        ('solutions', '0010_sitezsolution_delete_sitesolution'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.site'),
        ),
    ]
