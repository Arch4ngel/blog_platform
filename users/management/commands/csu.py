from django.core.management import BaseCommand

from users.models import User


class Command (BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            phone='79990001234',
            nickname='Admin',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            phone_verified=True,
            is_subscribed=True
            )
        user.set_password('12345')
        user.save()
