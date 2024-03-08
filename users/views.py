from django.shortcuts import render,redirect ,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from .form import RegisterCustomerForm , UpdateCustomerForm , UpdatePasswordForm , SetNewPasswordForm
from .models import User
from ticket.models import Ticket
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from solutions.models import Solution

def register_customer(request):
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_customer = True
            var.save()
            messages.info(request, 'Your account has been successfully registered. Please login to continue')
            return redirect('login')
        else:
            messages.warning(request , 'Something went wrong. please check form inputs')
            return redirect('register-customer')
    else :
        form = RegisterCustomerForm()
        context = {'form' : form}
        return render(request , 'users/register_customer.html' , context)
    

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request , username=username , password=password)
        if user is not None and user.is_active:
            login(request,user)
            messages.info(request , 'Login successfull. Please enjoy your session')
            return redirect('dashboard')
        else :
            messages.warning(request ,'Something went wrong. Please check form input')
            return redirect('login')
    else:
        return render(request , 'users/login.html')

@login_required
def logout_user(request):
    logout(request)
    messages.info(request, 'Your session has ended. Please log in to continue')
    return redirect('login')

@login_required
def home(request , slug):
    user = get_object_or_404(User , username=slug)
    tickets = Ticket.objects.filter(created_by = user).order_by('-date_created')
    friends = User.objects.filter(is_engineer = True).exclude(username = slug)
    solutions = Solution.objects.filter(owner = user)
    return render(request , 'users/home_customer.html' , {
        'user' : user,
        'friends': friends,
        'solutions' : solutions,
        'tickets' : tickets,
    })
    
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateCustomerForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your Profile info info has been updated and all the changes are saved in the Database')
            return redirect(f'/accounts/{request.user.username}')
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
    form = UpdateCustomerForm(instance=request.user)
    return render(request, 'users/update_profile.html' , {
        'form':form,
    })

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
@login_required
def update_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            test = form.save()
            update_session_auth_hash(request, test)
            messages.info(request, 'Your Password info has been changed !')
            return redirect(f'/accounts/{request.user.username}')
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
    form = PasswordChangeForm(request.user)
    return render(request, 'users/update_profile.html' , {
        'form':form,
    })
