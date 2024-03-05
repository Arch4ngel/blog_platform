from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    phone = models.CharField(unique=True, max_length=35, verbose_name='Телефон')

    nickname = models.CharField(max_length=35, verbose_name='Никнейм', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name="Пользователь активен")
    phone_verified = models.BooleanField(default=False, verbose_name='Верификация телефона')
    is_subscribed = models.BooleanField(default=False, verbose_name='Признак платной подписки')

    ver_code = models.CharField(max_length=15, default='', verbose_name='Проверочный код')

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.phone}'
