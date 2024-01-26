from django.shortcuts import render
from .models import WorkRecord
import datetime
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from  django.contrib import messages
from .models import Category, Solution
from users.models import User
from django.contrib.auth.decorators import login_required
from ticket.models import *
from .form import WorkRecordForm
from ticket.models import Ticket
from django.db.models import Sum

@login_required
def new(request):
    if request.user.is_engineer :
        if request.method == 'POST':
            form = WorkRecordForm(None , None or request.POST)
            if form.is_valid():
                var = form.save(commit=False)
                var.labor = request.user
                var.writer = request.user
                var.date_created = datetime.datetime.now()
                var.save()
                messages.info(request, 'Your solution has been successfully submitted Thanks!')
                return redirect('time-history')
            else:
                messages.warning(request, 'Something went wrong. Please check form input')
                return redirect('time-history')
        else:
            form = WorkRecordForm(uzer=request.user)
            return render(request, 'timemgmt/new_time.html' , {
                'form' : form,
            })
    else :
        return HttpResponse('Not Enought Permission')

@login_required
def history(request):
    records = WorkRecord.objects.filter(labor = request.user).order_by('-date_created')
    sum = records.aggregate(Sum('length_minute'))
    return render(request, 'timemgmt/history.html' , {
        'records': records,
        'sum': sum,
    })

@login_required
def delete (request , pk) :
    record = get_object_or_404(WorkRecord , pk=pk)
    if request.user == record.writer :
        record.delete()
        messages.info(request, 'record has been successfuly deleted!')
        return redirect('time-history')
    else :
        return HttpResponse('Not Enought Permission')