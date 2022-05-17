from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from rest_framework.authtoken.models import Token

from user.models import User
from fixtures.users.factory import create_fake_info


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def assign_staff_status(sender, instance: User, **kwargs):
    if instance.role > User.TAXPAYER:
        instance.is_staff = True
    if instance.role == User.ADMIN:
        instance.is_superuser = True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_info_and_token(sender, instance: User = None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        create_fake_info(instance.id, instance.last_name)
