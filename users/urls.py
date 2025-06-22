from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register-customer' , views.register_customer , name='register-customer'),
    path('login' , views.login_user , name='login'),
    path('logout' , views.logout_user , name='logout'),
    path('<slug:slug>' , views.home , name='home'),
    path('update-profile/' , views.update_profile , name='update-profile'),
    path('update-password/' , views.update_password , name='update-password'),
    path('password-reset/', ResetPasswordView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/PasswordReset/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/PasswordReset/password_reset_complete.html'),
         name='password_reset_complete'),
]
