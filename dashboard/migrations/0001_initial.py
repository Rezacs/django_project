# Generated by Django 4.2.7 on 2023-12-11 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('solutions', '0007_category_parent'),
        ('users', '0006_site_slug_alter_site_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(default='Write something')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField()),
                ('file', models.FileField(blank=True, null=True, upload_to='announcement_file')),
                ('number', models.UUIDField(default=uuid.uuid4)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='solutions.category')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.site')),
            ],
        ),
    ]