import random
import requests
from django.conf import settings
from django.shortcuts import redirect


def send_text(phone, message):
    response = requests.post(settings.SMS_API_URL, json={'number': phone, 'text': message, 'sign': 'SMS Aero'})
    return response


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_text(
        phone=request.user.phone,
        message=f'Ваш новый пароль {new_password}'
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect('users:login')
