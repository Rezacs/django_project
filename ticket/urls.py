from django.urls import path
from . import views

urlpatterns = [
    path('ticket-details/<slug:slug>/', views.ticket_details, name='ticket-details'),
    path('create-ticket/', views.create_ticket , name='create-ticket' ),
    path('update-ticket/<slug:slug>/', views.update_ticket, name='update-ticket'),
    path('all-tickets/', views.all_tickets  , name='all-tickets' ),
    path('ticket-queue/' , views.ticket_queue , name='ticket-queue' ),
    path('accept-ticket/<slug:slug>/' , views.accept_ticket , name='accept-ticket' ),
    path('close-ticket/<slug:slug>/', views.close_ticket , name='close-ticket' ),
    path('workspace/' , views.workspace , name='workspace' ),
    path('all-closed-tickets/', views.all_closed_tickets , name='all-closed-tickets' ),
    path('remove-assignement/<slug:slug>/', views.remove_assignement , name='remove-assignement' ), 
    path('create-ticket/<int:pk>/', views.create_ticket_category , name='create-ticket-category' ),
    path('delete-ticket/<slug:slug>/', views.delete_ticket , name='delete-ticket' ),
    path('gpt-ticket/<slug:slug>/', views.gpt_ticket_chat, name='gpt-ticket-api'),
]
