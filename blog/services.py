import stripe
from django.conf import settings
from stripe import InvalidRequestError

from blog.models import Payment


def check_payment(user):
    """Функция проверяет, есть ли среди завершенных сессий оплаты Stripe
    успешный платеж по номеру телефона пользователя. В случае удачной проверки пользователю устанавливается статус
    подписчика и создается экземпляр класса платежа."""
    try:
        stripe.api_key = settings.STRIPE_API_KEY
        response = stripe.Event.list(type='checkout.session.completed')
        new_payment = None
        for item in response["data"]:
            if (item["data"]['object']["customer_details"]['phone'][1:] == user.phone
                    and item["data"]['object']['payment_status'] == 'paid'):
                user.is_subscribed = True
                user.save()
                new_payment = Payment.objects.create(
                    user=user,
                    transaction_id=item["data"]['object']['id']
                )
        return new_payment
    except stripe.error.InvalidRequestError:
        raise InvalidRequestError(param=None, message='Платеж не найден')
