import random
import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from users.models import User


def send_text(phone, message):
    response = requests.post(settings.SMS_API_URL, json={'number': phone, 'text': message, 'sign': 'SMS Aero'})
    return response


def generate_new_password(phone):
    try:
        user = User.objects.get(phone=phone)
        new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        send_text(
            phone=user.phone,
            message=f'Ваш новый пароль {new_password}'
        )
        user.set_password(new_password)
        user.save()
    except ObjectDoesNotExist:
        ObjectDoesNotExist('Пользователь не найден')
