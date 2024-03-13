from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError

from users.models import User


class UserLoginForm(AuthenticationForm):
    """Форма входа в систему"""
    class Meta:
        model = User
        fields = ['phone', 'password']

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': '7999...'})
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя"""
    class Meta:
        model = User
        fields = ['phone', 'nickname', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].widget = forms.TextInput(attrs={'placeholder': '7999...'})
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_phone(self):
        """Проверка корректности номера"""
        cleaned_data = self.cleaned_data.get('phone')
        if not cleaned_data[0] == '7' or len(cleaned_data) != 11:
            raise ValidationError("Введите корректный номер!")
        return cleaned_data


class UserProfileForm(UserChangeForm):
    """Форма редактирования профиля"""
    class Meta:
        model = User
        fields = ['nickname']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class NewpasswordForm(forms.Form):
    """Форма восстановления пароля"""
    phone = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'placeholder': '7999...'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_phone(self):
        """Проверка существования пользователя"""
        cleaned_data = self.cleaned_data.get('phone')
        if not User.objects.filter(phone=cleaned_data):
            raise ValidationError("Пользователь не найден!")
        return cleaned_data
