from  django.contrib import messages
from django.shortcuts import get_object_or_404, render , redirect
from .form import SurveyForm
from .models import Survey

def survey_new_record(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            code = form.cleaned_data['student_code']
            if Survey.objects.filter(student_code=code) :
                messages.warning(request, 'You have filled the form once! cant submit again')
                return redirect('dashboard')
            var.save()
            messages.info(request, 'Your ticket has been successfully submitted. An engineer would be assigned soon!')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('dashboard')
    else:
        form = SurveyForm()
        return render(request, 'users/survey.html' , {
            'form' : form
        })
