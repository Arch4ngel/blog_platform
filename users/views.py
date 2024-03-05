import random
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from users.services import send_text


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verify_phone')

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save()
            new_user.ver_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            send_text(
                phone=new_user.phone,
                message=f'Код подтверждения {new_user.ver_code}',
            )
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class VerificationTemplateView(TemplateView):
    template_name = 'users/verify_phone.html'

    def post(self, request):
        ver_code = request.POST.get('ver_code')
        user_code = User.objects.filter(ver_code=ver_code).first()

        if user_code is not None and user_code.ver_code == ver_code:
            user_code.is_active = True
            user_code.save()
            return redirect('users:login')
        else:
            return redirect('users:verify_phone_error')


class VerificationErrorTemplateView(VerificationTemplateView):
    template_name = 'users/verify_phone_error.html'
