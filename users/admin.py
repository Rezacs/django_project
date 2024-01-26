from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User , Site

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom Field Heading',
            {
                'fields': (
                    'is_customer',
                    'is_engineer',
                    'image',
                    'site',
                    'contact',
                    'ssites',
                )
            }
        )
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Site)