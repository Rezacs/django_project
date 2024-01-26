from django.urls import path
from . import views

urlpatterns = [
    path('' , views.dashboard, name='dashboard'),
    path('announcement/<slug:slug>/' , views.announcement_view, name='announcement'),
    path('announcement' , views.create_announce, name='create-announcement'),
    path('user-announcement' , views.create_user_announce, name='create-user-announcement'),
    path('update-announcement/<slug:slug>/' , views.update_announcement, name='update-announcement'),
    path('delete-announcement/<int:pk>/' , views.delete_announcement, name='delete-announcement'),
    path('targeted-announcement/<slug:slug>/' , views.create_direct_user_announce, name='targeted-announcement'),
    path('site/<slug:slug>/' , views.create_direct_user_announce, name='site'),
]