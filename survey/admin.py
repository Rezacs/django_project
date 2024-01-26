from django.contrib import admin
from .models import Survey

# admin.site.register(Survey)

@admin.register(Survey)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("student_name", "student_code", "subject", "date_created")
