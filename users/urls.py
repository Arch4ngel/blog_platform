from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.forms import UserLoginForm
from users.views import *

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html', form_class=UserLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify_phone/', VerificationTemplateView.as_view(), name='verify_phone'),
    path('verify_phone_error/', VerificationErrorTemplateView.as_view(), name='verify_phone_error'),
    path('password_recovery/', ForgotPasswordFormView.as_view(), name='password_recovery'),
]
