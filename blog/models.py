from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Пользователь',
                             **NULLABLE)

    title = models.CharField(max_length=50, verbose_name='Заголовок')
    slug = models.CharField(max_length=50, verbose_name='slug')
    body = models.TextField(verbose_name='Текст')
    image = models.ImageField(upload_to='posts/', verbose_name='Изображение', **NULLABLE)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_private = models.BooleanField(verbose_name='Пост для платной подписки', default=False)
    views_count = models.IntegerField(verbose_name='Количество просмотров', default=0)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Payment(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Пользователь',
                             **NULLABLE)
    transaction_id = models.TextField(verbose_name='Идентификатор платежа', **NULLABLE)
    dateime = models.DateTimeField(auto_now_add=True, verbose_name='Время платежа')
    amount = models.PositiveIntegerField(verbose_name='Сумма', default=100)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
