from django.contrib import admin
from .models import Announcement

class AnnouncementAdmin(admin.ModelAdmin) :
    list_display = ('title' , 'owner' , 'site' , 'target' )

admin.site.register(Announcement , AnnouncementAdmin)
