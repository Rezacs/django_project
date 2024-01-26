from django.urls import path
from . import views

urlpatterns = [
    path('new' , views.new , name='time-new'),
    path('history' , views.history , name='time-history'),
    path('delete/<int:pk>' , views.delete , name='time-delete'),
]
