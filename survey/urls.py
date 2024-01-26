from django.urls import path
from . import views

urlpatterns = [
    path('', views.survey_new_record, name='survey'),
]
