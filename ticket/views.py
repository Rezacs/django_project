import datetime
from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from  django.contrib import messages
from .models import Ticket
from .form import *
from users.models import User
from django.contrib.auth.decorators import login_required
from solutions.models import Category
from django.db.models import Q

@login_required
def ticket_details(request , slug):
    ticket = Ticket.objects.get(number=slug)
    if request.user.is_engineer or request.user == ticket.created_by :
        t = User.objects.get(username=ticket.created_by)
        # tickets_per_user = Ticket.objects.filter(created_by=t)
        tickets_per_user = t.created_by.all().exclude(number = slug)
        # tickets_per_user = Ticket.objects.filter(created_by=t and pk != pk)
        context = {'ticket':ticket, 'tickets_per_user':tickets_per_user}
        return render(request, 'ticket/ticket_details.html', context)
    else :
        return HttpResponse('Not Enought Permission')

"""For Customers"""
@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            var.ticket_status = 'Pending'
            var.site = request.user.site
            var.save()
            messages.info(request, 'Your ticket has been successfully submitted. An engineer would be assigned soon!')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = {'form':form}
        return render(request, 'ticket/create_ticket.html' , context)
    
@login_required
def create_ticket_category(request , pk):
    category = get_object_or_404(Category , pk=pk)
    if request.method == 'POST':
        form = CreateTicketCategoryForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            var.ticket_status = 'Pending'
            var.category = category
            var.save()
            messages.info(request, f'Your ticket has been successfully submitted in {category.title} category')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('create-ticket')
    else:
        form = CreateTicketCategoryForm()
        context = {'form':form}
        return render(request, 'solutions/create_ticket_category.html' , context)
    

@login_required
def update_ticket(request, slug):
    ticket = get_object_or_404(Ticket,number = slug)
    if request.user == ticket.created_by or request.user.is_engineer :
        if not ticket.is_resolved :
            if request.method == 'POST':
                form = UpdateTicketForm(request.POST, instance=ticket)
                if form.is_valid():
                    form.save()
                    messages.info(request, 'Your ticket info has been updated and all the changes are saved in the Database')
                    return redirect('dashboard')
                else:
                    messages.warning(request, 'Something went wrong. Please check form input')
                    return redirect('create-ticket')
            else:
                form = UpdateTicketForm(instance=ticket)
                context = {'form':form}
                return render(request, 'ticket/update_ticket.html' , context)
    return HttpResponse('Not Enought Permission')

    
def all_tickets(request):
    tickets = Ticket.objects.filter(created_by=request.user).order_by('-date_created')
    context = {'tickets':tickets}
    return render(request, 'ticket/all_tickets.html' , context)


"""For Engineers"""
@login_required
def ticket_queue(request):
    sites = request.user.ssites.all()
    tickets = Ticket.objects.filter(ticket_status='Pending')
    unrelated_ticket = tickets.exclude(created_by__site__in = sites)
    your_sites_tickets = tickets.filter(created_by__site__in = sites)
    return render(request, 'ticket/ticket_queue.html' , {
        'tickets' : unrelated_ticket,
        'sites' :sites,
        'your_tickets':your_sites_tickets,
    })


@login_required
def accept_ticket(request, slug):
    if request.user.is_engineer :
        ticket = Ticket.objects.get(number=slug)
        ticket.assigned_to = request.user
        ticket.ticket_status = 'Active'
        ticket.accepted_date = datetime.datetime.now()
        ticket.save()
        messages.info(request, 'Ticket has been accepted. Please resolve as soon as possible!')
        return redirect(f'/ticket/ticket-details/{ticket.number}')
    else :
        return HttpResponse('Not Enought Permission')

@login_required
def close_ticket(request, pk):
    if request.user.is_engineer :
        ticket = Ticket.objects.get(pk=pk)
        ticket.ticket_status = 'Completed'
        ticket.solver = request.user
        ticket.is_resolved=True
        ticket.closed_date = datetime.datetime.now()
        ticket.save()
        messages.info(request, 'Ticket has been resolved. Thank you brilliant support Engineer!')
        return redirect('ticket-queue')
    else :
        return HttpResponse('Not Enought Permission')

@login_required
def workspace(request):
    tickets = Ticket.objects.filter(assigned_to=request.user , is_resolved=False)
    context = {'tickets':tickets}
    return render(request, 'ticket/workspace.html' , context)

@login_required
def all_closed_tickets(request):
    if request.user.is_engineer :
        tickets = Ticket.objects.filter(Q(solver=request.user, is_resolved=True) | Q(assigned_to=request.user, is_resolved=True))
        context = {'tickets':tickets}
        return render(request, 'ticket/all_closed_tickets.html', context)
    else :
        return HttpResponse('Not Enought Permission')

@login_required
def remove_assignement (request , slug):
    if request.user.is_engineer :
        ticket = Ticket.objects.get(number=slug)
        ticket.ticket_status = 'Pending'
        ticket.assigned_to = None
        ticket.is_resolved=False
        ticket.save()
        messages.info(request, 'Ticket Assignement has been removed!')
        return redirect('ticket-queue')
    else :
        return HttpResponse('Not Enought Permission')
    
@login_required
def delete_ticket (request , slug) :
    ticket = get_object_or_404(Ticket , number=slug)
    if request.user == ticket.created_by :
        ticket.delete()
        messages.info(request, 'Ticket has been successfuly deleted!')
        return redirect('all-tickets')
    else :
        return HttpResponse('Not Enought Permission')

