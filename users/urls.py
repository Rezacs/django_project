from django.urls import path
from . import views

urlpatterns = [
    path('register-customer' , views.register_customer , name='register-customer'),
    path('login' , views.login_user , name='login'),
    path('logout' , views.logout_user , name='logout'),
    path('<slug:slug>' , views.home , name='home'),
    path('update-profile/' , views.update_profile , name='update-profile'),
    path('update-password/' , views.update_password , name='update-password'),
]
