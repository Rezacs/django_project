import datetime
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from  django.contrib import messages
from .models import Category, Solution
from users.models import User
from django.contrib.auth.decorators import login_required
from ticket.models import *
from .form import SolutionForm, SuggestSolution
from ticket.models import Ticket

@login_required
def view_categories(request):
    categories = Category.objects.all()
    return render(request, 'solutions/categories.html', {
        'categories':categories,
    })

@login_required
def category_detail(request , pk):
    category = get_object_or_404(Category , pk=pk)
    sub_categories = Category.objects.filter(parent=category)
    # parents = Category.objects.filter(parent__in = category )
    if request.user.is_engineer :
        solutions = Solution.objects.filter(category = category).filter(visible_to_all = True)
        site_solutions = Solution.objects.filter(site = request.user.site).filter(visible_to_all = False).filter(category = category)
    else :
        solutions = Solution.objects.filter(category = category).filter(visible = True).filter(visible_to_all = True)
        site_solutions = Solution.objects.filter(site = request.user.site).filter(visible = True).filter(visible_to_all = False).filter(category = category)
    your_tickets = Ticket.objects.filter(created_by = request.user).filter(category = category)
    return render(request, 'solutions/category.html', {
        'category':category,
        'solutions' : solutions,
        'your_tickets' : your_tickets,
        'sub_categories' : sub_categories,
        'site_solutions' : site_solutions,
    })  

@login_required
def view_solution(request , pk) :
    solution = get_object_or_404( Solution , pk=pk)
    more_solutions = Solution.objects.filter(category = solution.category)
    solution.last_viewed = datetime.datetime.now()
    citations = Ticket.objects.filter(solution = solution)
    return render(request, 'solutions/solution.html', {
        'solution':solution,
        'more_solutions' : more_solutions,
        'citations' : citations,
    })

@login_required
def new_solution(request, pk):
    category = get_object_or_404(Category , pk=pk)
    if request.user.is_engineer :
        if request.method == 'POST':
            form = SolutionForm(request.POST , request.FILES)
            if form.is_valid():
                var = form.save(commit=False)
                var.owner = request.user
                var.category = category
                var.date_created = datetime.datetime.now()
                var.save()
                messages.info(request, 'Your solution has been successfully submitted Thanks!')
                return redirect(f'/categories/{category.id}')
            else:
                messages.warning(request, 'Something went wrong. Please check form input')
                return redirect(f'/categories/{category.id}')
        else:
            form = SolutionForm()
            return render(request, 'solutions/create_solution.html' , {
                'form' : form,
                'category' : category,
            })
    else :
        return HttpResponse('Not Enought Permission')
    
@login_required
def remove_solution(request , pk):
    solution = get_object_or_404(Solution , pk=pk)
    category = solution.category
    if request.user == solution.owner :
        solution.delete()
        messages.info(request, 'Your solution has been successfully Removed!')
        return redirect(f'/categories/{category.id}')
    else :
        return HttpResponse('Not Enought Permission')

@login_required
def update_solution(request, pk):
    solution = get_object_or_404(Solution , pk=pk)
    if request.user == solution.owner :
        if request.method == 'POST':
            form = SolutionForm(request.POST, request.FILES, instance=solution)
            if form.is_valid():
                form.save()
                messages.info(request, 'Your solution info has been updated and all the changes are saved in the Database')
            else:
                messages.warning(request, 'Something went wrong. Please check form input')
            return redirect(f'/categories/solution/{solution.pk}')
        else:
            form = SolutionForm(instance=solution)
            return render(request, 'solutions/update_solution.html' , {
                'form':form,
            })
    else :
        return HttpResponse('Not Enought Permission')
    
@login_required
def suggest_solution(request , slug):
    ticket = get_object_or_404(Ticket , number=slug)
    if request.user.is_engineer :
        if request.method == 'POST':
            form = SuggestSolution(request.POST, request.FILES, instance=ticket)
            if form.is_valid():
                form.save()
                messages.info(request, 'Your solution info has been advised for that ticket')
            else:
                messages.warning(request, 'Something went wrong. Please check form input')
            return redirect(f'/ticket/ticket-details/{ticket.number}')
        else:
            form = SuggestSolution(instance=ticket)
            return render(request, 'solutions/suggest_solution.html' , {
                'form':form,
                'ticket':ticket,
            })     
    else :
        return HttpResponse('Not Enought Permission')
    
@login_required
def new_site_solution(request, pk):
    category = get_object_or_404(Category , pk=pk)
    if request.user.is_engineer :
        if request.method == 'POST':
            form = SolutionForm(request.POST , request.FILES)
            if form.is_valid():
                var = form.save(commit=False)
                var.owner = request.user
                var.category = category
                var.date_created = datetime.datetime.now()
                var.site = request.user.site
                var.visible_to_all = False
                var.save()
                messages.info(request, 'Your solution for your SITE has been successfully submitted Thanks!')
                return redirect(f'/categories/{category.id}')
            else:
                messages.warning(request, 'Something went wrong. Please check form input')
                return redirect(f'/categories/{category.id}')
        else:
            form = SolutionForm()
            return render(request, 'dashboard/create_announce.html' , {
                'form' : form,
                'category' : category,
            })
    else :
        return HttpResponse('Not Enought Permission')