from django import forms
from .models import WorkRecord 
from users.models import Site

class WorkRecordForm(forms.ModelForm):
    class Meta:
        model = WorkRecord
        fields = ['site', 'date', 'start' , 'end']
    def __init__(self, uzer = None , *args, **kwargs):
        super(WorkRecordForm, self).__init__(*args, **kwargs)
        if self.instance:
            if uzer :
                self.fields['site'].queryset = Site.objects.filter(pk__in = uzer.ssites.all()).exclude(pk = uzer.pk)

# class SuggestSolution(forms.ModelForm):
#     class Meta:
#         model = Ticket
#         fields = ['solution']
#     def __init__(self , *args, **kwargs):
#         super(SuggestSolution, self).__init__(*args, **kwargs)
#         self.fields['solution'].queryset = Solution.objects.filter(visible = True)
