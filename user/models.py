from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ADMIN = 2
    TAXPAYER = 0
    TAXACCOUNTANT = 1

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (TAXPAYER, 'Taxpayer'),
        (TAXACCOUNTANT, 'Taxaccountant'),
    )

    role = models.SmallIntegerField(choices=ROLE_CHOICES, default=TAXPAYER)

    def __str__(self) -> str:
        return f'{self.username} - {self.get_role_display()}'


class Info(models.Model):
    """
    Info is a "meta" table for users. It contains
    all the tax information for the user. Why not store
    all this in User model? To avoid a wide table.
    """

    address = models.CharField(max_length=255, null=True)
    business_name = models.CharField(max_length=255, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    pan = models.CharField(
        'Pan No.', max_length=10, null=True, help_text='10 digit long alphanumeric code'
    )
    state = models.ForeignKey(
        'tax.State', on_delete=models.CASCADE, related_name='residents', null=True
    )
    gstin = models.CharField(
        'GST No.',
        max_length=15,
        null=True,
        help_text='15 digit long alphanumeric code derived from pan no.',
    )

    class Meta:
        verbose_name = 'Information'
        verbose_name_plural = 'Information'

    def __str__(self) -> str:
        return f'#{self.user_id} - {self.pan}'
