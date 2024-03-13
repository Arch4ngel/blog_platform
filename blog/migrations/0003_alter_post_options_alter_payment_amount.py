# Generated by Django 5.0.3 on 2024-03-13 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_user_payment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-date_created'], 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.PositiveIntegerField(default=100, verbose_name='Сумма'),
        ),
    ]