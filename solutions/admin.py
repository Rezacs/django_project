from django.contrib import admin
from . models import *

class SolutionAdmin(admin.ModelAdmin) :
    list_display = ('title' , 'owner' , 'site' , 'pk')

admin.site.register(Category)
admin.site.register(Solution , SolutionAdmin)
