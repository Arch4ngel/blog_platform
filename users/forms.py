from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.core.exceptions import ValidationError

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['phone', 'nickname', 'password1', 'password2']


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['nickname']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class NewpasswordForm(forms.Form):
    phone = forms.CharField(label='Номер телефона')

    def clean_phone(self):
        cleaned_data = self.cleaned_data.get('phone')
        if not User.objects.filter(phone=cleaned_data):
            raise ValidationError("Пользователь не найден!")
        return cleaned_data
