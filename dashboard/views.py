from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Announcement
from ticket.models import *
from django.db.models import Q
import datetime
from .form import CreateAnnouncementForm, CreateUserAnnouncementForm,CreateDirectTargetAnnouncementForm
from  django.contrib import messages
from django.urls import reverse

@login_required
def dashboard(request):
    if request.user.is_engineer :
        site_announcements = Announcement.objects.filter(site = request.user.site)
        user_announcements = Announcement.objects.filter(owner = request.user)
        return render(request , 'dashboard/dashboard.html' , {
            'site_announcements' : site_announcements,
            'user_announcements' : user_announcements,
        })
    else :
        now = datetime.datetime.now()
        site_announcements = Announcement.objects.filter(site = request.user.site)
        target_announcements = Announcement.objects.filter(target = request.user)
        tickets = Ticket.objects.filter(created_by = request.user)
        active_tickets = tickets.filter(ticket_status = 'Active')
        pending_tickets = tickets.filter(ticket_status = 'Pending')
        return render(request , 'dashboard/dashboard.html' , {
            'site_announcements' : site_announcements,
            'target_announcements' : target_announcements,
            'active_tickets' : active_tickets,
            'pending_tickets' : pending_tickets,
        })

@login_required
def announcement_view(request , slug):
    announcement = get_object_or_404(Announcement , number = slug)
    return render(request , 'dashboard/announcement.html' , {
        'announcement':announcement,
    })

@login_required
def create_announce(request):
    if request.user.is_engineer : 
        if request.method == 'POST':
            form = CreateAnnouncementForm(None , None or request.POST, request.FILES)
            if form.is_valid():
                var = form.save(commit=False)
                var.owner = request.user
                if not var.target :
                    var.site = request.user.site
                var.save()
                messages.info(request, 'Your Announcement has been successfully submitted. An engineer would be assigned soon!')
                return redirect('dashboard')
            else:
                messages.warning(request, 'Something went wrong. Please check form input')
                return redirect('dashboard')
        else:
            form = CreateAnnouncementForm(uzer=request.user)
            return render(request, 'dashboard/create_announce.html' , {
                'form' : form,
            })
    else :
        return HttpResponse('Not Enought Permission')
    
@login_required
def create_user_announce(request):
    if request.user.is_engineer : 
        if request.method == 'POST':
            form = CreateUserAnnouncementForm(None , None or request.POST, request.FILES)
            if form.is_valid():
                var = form.save(commit=False)
                var.owner = request.user
                if not var.target :
                    var.site = request.user.site
                var.save()
                messages.info(request, 'Your Announcement has been successfully submitted. An engineer would be assigned soon!')
                return redirect('dashboard')
            else:
                messages.warning(request, 'Something went wrong. Please check form input')
                return redirect('dashboard')
        else:
            form = CreateUserAnnouncementForm(uzer=request.user)
            return render(request, 'dashboard/create_announce.html' , {
                'form' : form,
            })
    else :
        return HttpResponse('Not Enought Permission')
    
@login_required
def update_announcement(request, slug):
    announcement = get_object_or_404(Announcement,number = slug)
    if request.user == announcement.owner :
        if request.method == 'POST':
            form = CreateAnnouncementForm(request.POST, request.FILES, instance=announcement)
            if form.is_valid():
                form.save()
                messages.info(request, 'Your ticket info has been updated and all the changes are saved in the Database')
                return redirect(f'/announcement/{announcement.number}/')
            else:
                messages.warning(request, 'Something went wrong. Please check form input')
                return redirect('create-ticket')
        else:
            form = CreateAnnouncementForm(instance=announcement)
            return render(request, 'dashboard/create_announce.html' , {
                'form':form,
            })
    else :
        return HttpResponse('Not Enought Permission')
    
@login_required
def delete_announcement(request , pk) :
    announcement = get_object_or_404(Announcement,pk = pk)
    if request.user == announcement.owner :
        announcement.delete()
        messages.info(request, 'Announcement has been successfuly deleted!')
        # return reverse("dashboard")
        return redirect('dashboard')
    else :
        return HttpResponse('Not Enought Permission')

@login_required
def create_direct_user_announce(request , slug):
    target = get_object_or_404(User , username=slug)
    if request.user.is_engineer : 
        if request.method == 'POST':
            form = CreateDirectTargetAnnouncementForm(request.POST, request.FILES)
            if form.is_valid():
                var = form.save(commit=False)
                var.owner = request.user
                var.target = target
                var.save()
                messages.info(request, 'Your Announcement has been successfully submitted to target')
                return redirect('dashboard')
            else:
                messages.warning(request, 'Something went wrong. Please check form input')
                return redirect('dashboard')
        else:
            form = CreateDirectTargetAnnouncementForm()
            return render(request, 'dashboard/create_announce.html' , {
                'form' : form,
            })
    else :
        return HttpResponse('Not Enought Permission')
    