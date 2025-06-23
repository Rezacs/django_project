import os
import openai
import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from  django.contrib import messages
from .models import Ticket
from .form import *
from users.models import User
from django.contrib.auth.decorators import login_required
from solutions.models import Category
from django.db.models import Q
from django.views.decorators.http import require_POST

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



OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Set this in your environment, never hardcode!
client = openai.OpenAI(api_key=OPENAI_API_KEY)

"""For Customers"""
@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        print("Form received. Is valid?", form.is_valid())
        if form.is_valid():
            cleaned = form.cleaned_data
            title = cleaned.get('title')
            description = cleaned.get('description')
            category = cleaned.get('category')
            print(f"User input -- Title: {title} | Category: {category} | Description: {description}")

            # If title or category is missing, ask AI
            if not title or not category:
                prompt = (
                    f"You are a helpful IT support engineer. "
                    f"The ticket description is: {description}\n"
                    f"Please generate a concise and accurate ticket title and suggest an appropriate category name "
                    f"based on this description. "
                    f"Output in this format:\nTitle: ...\nCategory: ..."
                )
                print("AI PROMPT:\n", prompt)
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are a helpful IT support engineer for a managed IT services company."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    ai_answer = response.choices[0].message.content.strip()
                    print("AI RAW RESPONSE:", ai_answer)
                    lines = ai_answer.splitlines()
                    ai_title = None
                    ai_category_name = None
                    for line in lines:
                        print("Parsing line:", line)
                        if line.lower().startswith("title:"):
                            ai_title = line.partition(":")[2].strip()
                        elif line.lower().startswith("category:"):
                            ai_category_name = line.partition(":")[2].strip()
                    print(f"AI Parsed -- Title: {ai_title} | Category: {ai_category_name}")
                    if not title and ai_title:
                        title = ai_title
                    if not category and ai_category_name:
                        category_obj, created = Category.objects.get_or_create(title=ai_category_name)
                        category = category_obj
                except Exception as e:
                    print("AI EXCEPTION:", e)
                    messages.warning(request, f"AI failed to generate title/category: {str(e)}")
                    return redirect('create-ticket')

            print(f"Final values -- Title: {title} | Category: {category}")

            if not title:
                print("Final error: Missing title.")
                messages.warning(request, "A title is required, and AI could not generate one.")
                return redirect('create-ticket')
            if not category:
                print("Final error: Missing category.")
                messages.warning(request, "A category is required, and AI could not generate one.")
                return redirect('create-ticket')

            # Now create and save the ticket object
            var = form.save(commit=False)
            var.title = title
            var.category = category
            var.created_by = request.user
            var.ticket_status = 'Pending'
            var.site = request.user.site
            var.save()
            print(f"Ticket saved: {var}")
            messages.info(request, "Your ticket has been successfully submitted. An engineer will be assigned soon!")
            return redirect('dashboard')

        else:
            print("Form errors:", form.errors)
            messages.warning(request, "Something went wrong. Please check form input.")
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = {'form': form}
        return render(request, 'ticket/create_ticket.html', context)



    
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
def close_ticket(request, slug):
    if request.user.is_engineer :
        ticket = Ticket.objects.get(number=slug)
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
    



@login_required
@require_POST
def gpt_answer_api(request):
    category = request.POST.get('category') or request.body.get('category')
    title = request.POST.get('title') or request.body.get('title')
    description = request.POST.get('description') or request.body.get('description')
    number = request.POST.get('number')
    user = request.POST.get('created_by')
    ticket = request.POST.get('ticket')

    # If using AJAX/JS, you'll likely send JSON: parse it
    import json
    try:
        data = json.loads(request.body.decode('utf-8'))
        category = data.get('category')
        title = data.get('title')
        description = data.get('description')
        number = data.get('number')
        user = data.get('user')
        ticket = data.get('ticket')
    except Exception:
        pass  # fallback to form-data

    prompt = (
        f"You are a helpful IT support engineer. "
        f"The ticket category is '{category}'.\n"
        f"Ticket title: {title}\n"
        f"Full description: {description}\n"
        f"Number of ticket is : {number} \n"
        f"Username who wrote ticket is : {user}\n\n"
        f"Please provide the most probable troubleshooting steps, solution, or reply to the user."
        f"You should answer in a way that the user doesnt understand you are AI. they should think you are a human "
    )

    answer = None
    error = None
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful IT support engineer for a managed IT services company."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content
    except Exception as e:
        error = str(e)

    context = {
        'category': category,
        'title': title,
        'description': description,
        'number': number,
        'user': user,
        'ticket' : ticket,
        'answer': answer,
        'error': error,
    }
    return render(request, 'ticket/gpt_answer.html', context)

@login_required
def gpt_ticket_chat(request, slug):
    ticket = get_object_or_404(Ticket, number=slug)
    chats = Chat.objects.filter(ticket=ticket).order_by("created_at")

    # Only allow the customer who created the ticket
    if request.user != ticket.created_by:
        return HttpResponse('Not enough permission')

    # --- STEP 1: Initiate first GPT message if chat is empty ---
    if not chats.exists():
        prompt = (
            f"You are a helpful IT support engineer. "
            f"Ticket category: {ticket.category}\n"
            f"Ticket title: {ticket.title}\n"
            f"Full description: {ticket.description}\n\n"
            f"You should answer in a way that the user doesn't realize you are an AI. Please answer naturally as a human IT engineer."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"My issue: {ticket.description}"}
                ],
            )
            gpt_reply = response.choices[0].message.content
        except Exception as e:
            gpt_reply = "Sorry, there was an error generating an initial reply. Please try again."

        # Save GPT's first message
        Chat.objects.create(
            ticket=ticket,
            user=request.user ,      # or a special AI user if you want
            content=gpt_reply,
            is_gpt=True
        )
        # Refresh chats queryset
        chats = Chat.objects.filter(ticket=ticket).order_by("created_at")

    # --- STEP 2: Handle user input and AI reply ---
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            # Save user message
            user_message = form.save(commit=False)
            user_message.ticket = ticket
            user_message.user = request.user
            user_message.is_gpt = False
            user_message.save()

            # Get full conversation for context (including new user message)
            chats = Chat.objects.filter(ticket=ticket).order_by("created_at")
            history = [{"role": "user" if not c.is_gpt else "assistant", "content": c.content} for c in chats]

            prompt = (
                f"You are a helpful IT support engineer. "
                f"Ticket category: {ticket.category}\n"
                f"Ticket title: {ticket.title}\n"
                f"Full description: {ticket.description}\n\n"
                f"You should answer in a way that the user doesn't realize you are an AI. Please answer naturally as a human IT engineer."
            )

            messages_for_gpt = [{"role": "system", "content": prompt}] + history

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages_for_gpt,
                )
                gpt_reply = response.choices[0].message.content
            except Exception as e:
                gpt_reply = "Sorry, there was an error generating a reply. Please try again."

            # Save GPT reply
            Chat.objects.create(
                ticket=ticket,
                user=request.user ,  # or your special AI user
                content=gpt_reply,
                is_gpt=True
            )
            messages.info(request, 'Your message was submitted!')
            return redirect(request.path)  # Refresh for live effect
    else:
        form = ChatForm()

    # Always re-fetch chats after any possible update
    chats = Chat.objects.filter(ticket=ticket).order_by("created_at")

    return render(request, 'ticket/gpt_answer.html', {
        'form': form,
        'chats': chats,
        'ticket': ticket,
        'category': ticket.category,
        'title': ticket.title,
        'description': ticket.description,
    })
