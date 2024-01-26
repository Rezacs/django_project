from django import forms
from .models import Solution 
from ticket.models import Ticket

class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ['title', 'description', 'file' , 'visible']

class SuggestSolution(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['solution']
    def __init__(self , *args, **kwargs):
        super(SuggestSolution, self).__init__(*args, **kwargs)
        self.fields['solution'].queryset = Solution.objects.filter(visible = True)
