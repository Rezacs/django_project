from django.urls  import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('ticket-chat/<slug:slug>/', views.new_conversation , name='ticket-chat'),
    path('news', views.latest_updates , name='news'),
    path('delete-chat/<int:pk>', views.delete_chat , name='delete-chat'),
]