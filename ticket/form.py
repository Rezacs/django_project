from django import forms
from .models import Ticket
from solutions.models import Solution

from chat.models import Chat

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['content']

class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['category'].required = False



class UpdateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description' , 'category']

class CreateTicketCategoryForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description']