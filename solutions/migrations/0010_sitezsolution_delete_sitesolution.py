# Generated by Django 4.2.7 on 2023-12-14 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0006_site_slug_alter_site_name'),
        ('solutions', '0009_alter_sitesolution_site'),
    ]

    operations = [
        migrations.CreateModel(
            name='SitezSolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visible', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(default='Write something')),
                ('last_viewed', models.DateTimeField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='solutions_file')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='solutions.category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.site')),
            ],
        ),
        migrations.DeleteModel(
            name='SiteSolution',
        ),
    ]
