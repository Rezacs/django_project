from django.contrib import admin , messages
from .models import WorkRecord
from django.utils.translation import ngettext

@admin.action(description='verify')
def make_published( request , queryset) :
    for obj in queryset :
        obj.verified = True
        obj.save()
        messages.success(request, "successfully done !")

class WorkRecordAdmin(admin.ModelAdmin):
    list_display = ("labor", "site", "date", "start" , "end" , "verified")
    list_filter = ("verified" , "site" , "date_created")
    actions = ["make_published"]


admin.site.register(WorkRecord , WorkRecordAdmin)




