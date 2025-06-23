from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render , get_object_or_404 , redirect
from ticket.models import *
from .models import Chat
from .forms import ChatForm
from  django.contrib import messages 


@login_required
def new_conversation(request , slug):
    ticket = get_object_or_404(Ticket , number=slug )

    if ticket.created_by == request.user or request.user.is_engineer :
        chats = Chat.objects.filter(ticket=ticket)

        if chats :
            pass # redirect to conversation

        if request.method == 'POST' :
            form = ChatForm(request.POST)
            if form.is_valid():
                conversation_message = form.save(commit=False)
                conversation_message.ticket = ticket
                conversation_message.user = request.user
                conversation_message.save()
                messages.info(request, 'Your message was submitted!')
                return redirect(f'/chat/ticket-chat/{ticket.number}')
        else :
            form = ChatForm()
        return render (request , 'chat/new.html' , {
            'form': form,
            'chats':chats,
            'ticket':ticket,
        } )
    else :
        return HttpResponse('Not Enought Permission')
    
@login_required
def latest_updates(request):
    if request.user.is_engineer :
        chats = Chat.objects.filter(user=request.user).order_by('created_at')
        tickets = Ticket.objects.filter(assigned_to = request.user)
        return render (request , 'chat/news.html' , {
            'chats': chats,
            'tickets':tickets,
        } )
    else :
        return HttpResponse('Not Enought Permission')
    
@login_required
def delete_chat(request , pk):
    chat = get_object_or_404(Chat , pk=pk)
    if request.user == chat.user :
        chat.delete()
        messages.success(request, 'Your message was deleted!')
        return redirect(f'/chat/ticket-chat/{chat.ticket.number}')
    else :
        return HttpResponse('Not Enought Permission')
    
