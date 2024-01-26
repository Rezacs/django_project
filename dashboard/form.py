from django import forms
from .models import Announcement
from users.models import *

class CreateAnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        exclude = ['owner' , 'date_created' , 'number' , 'target']
    def __init__(self, uzer = None , *args, **kwargs):
        super(CreateAnnouncementForm, self).__init__(*args, **kwargs)
        if self.instance:
            if uzer :
                self.fields['site'].queryset = Site.objects.filter(pk__in = uzer.ssites.all()).exclude(pk = uzer.pk)

class CreateUserAnnouncementForm (forms.ModelForm) :
    class Meta :
        model = Announcement
        exclude = ['site' , 'owner' , 'date_created' , 'number']
    def __init__(self , uzer = None , *args, **kwargs):
        super(CreateUserAnnouncementForm, self).__init__(*args, **kwargs)
        if self.instance:
            if uzer :
                self.fields['target'].queryset = User.objects.filter(site = uzer.site).exclude(pk = uzer.pk)

class CreateDirectTargetAnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        exclude = ['site' , 'owner' , 'date_created' , 'number' , 'target']