from django.urls import path
from . import views
from . models import Category

urlpatterns = [
    path('', views.view_categories, name='categories'),
    path('<int:pk>', views.category_detail, name='category'),
    path('solution/<int:pk>' , views.view_solution , name='solution'),
    path('new-solution/<int:pk>' , views.new_solution , name='create-solution'),
    path('delete-solution/<int:pk>' , views.remove_solution , name='delete-solution'),
    path('update-solution/<int:pk>' , views.update_solution , name='update-solution'),
    path('suggest-solution/<slug:slug>' , views.suggest_solution , name='suggest-solution'),
    path('new-site-solution/<int:pk>' , views.new_site_solution , name='create-site-solution'),
]