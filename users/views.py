import random
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, FormView

from users.forms import UserRegisterForm, UserProfileForm, NewpasswordForm
from users.models import User
from users.services import send_text, generate_new_password


# Create your views here.
class RegisterView(CreateView):
    """Пркдставление регистрации пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verify_phone')
    extra_context = {'title': 'Зарегистрироваться'}

    def form_valid(self, form):
        """Отправка и проверка кода подтверждения"""
        if form.is_valid():
            new_user = form.save()
            new_user.ver_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            send_text(
                phone=new_user.phone,
                message=f'Код подтверждения {new_user.ver_code}',
            )
        return super().form_valid(form)


class ProfileView(UpdateView):
    """Представление редактирования профиля"""
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('blog:blog')
    extra_context = {'title': 'Профиль'}

    def get_object(self, queryset=None):
        return self.request.user


class VerificationTemplateView(TemplateView):
    """Представление верификации телефона"""
    template_name = 'users/verify_phone.html'

    def post(self, request):
        ver_code = request.POST.get('ver_code')
        user_code = User.objects.filter(ver_code=ver_code).first()

        if user_code is not None and user_code.ver_code == ver_code:
            user_code.is_active = True
            user_code.phone_verified = True
            user_code.save()
            return redirect('users:login')
        else:
            return redirect('users:verify_phone_error')


class VerificationErrorTemplateView(VerificationTemplateView):
    """Представление ошибки верификации телефона"""
    template_name = 'users/verify_phone_error.html'


class ForgotPasswordFormView(FormView):
    """Представление сброса пароля"""
    template_name = 'users/password_recovery.html'
    form_class = NewpasswordForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        phone = form.cleaned_data['phone']
        generate_new_password(phone)
        return super().form_valid(form)
