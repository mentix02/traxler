from datetime import date

from django.db import models
from django.utils import timezone

from rest_framework.exceptions import ValidationError


class State(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=255)
    is_ut = models.BooleanField(default=False)
    tax = models.PositiveSmallIntegerField(help_text='Tax rate in percentage for state')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Tax(models.Model):

    STATUS_NEW = 'New'
    STATUS_PAID = 'Paid'
    STATUS_DELAYED = 'Delayed'

    due_date = models.DateField('Due date')
    paid = models.BooleanField(default=False)
    updated_on = models.DateField(auto_now=True)
    sgst = models.PositiveSmallIntegerField(
        'State tax', help_text='Tax rate in percentage for state'
    )
    payer = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='taxes',
    )

    @property
    def active_due(self):
        try:
            return self.history.get(active=True)
        except TaxDue.DoesNotExist:
            return None

    @property
    def status(self) -> str:
        today = timezone.now().date()
        if self.paid:
            return Tax.STATUS_PAID
        elif self.due_date < date(today.year, today.month, today.day):
            return Tax.STATUS_DELAYED
        else:
            return Tax.STATUS_NEW

    class Meta:
        verbose_name_plural = 'Taxes'

    def __str__(self) -> str:
        return f'{self.payer} - {self.active_due}'


class TaxDue(models.Model):

    TRANSACTION_INTERSTATE = True
    TRANSACTION_INTRASTATE = False

    TRANSACTION_TYPE_CHOICES = (
        (TRANSACTION_INTERSTATE, 'Interstate'),
        (TRANSACTION_INTRASTATE, 'Intrastate'),
    )

    active = models.BooleanField(default=True)
    issued_on = models.DateField(auto_now_add=True)
    salary_income = models.FloatField('Salary income')
    share_market_income = models.FloatField('Share market income')
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, related_name='history')
    cgst = models.PositiveSmallIntegerField(
        'Central tax',
        help_text='Tax rate in percentage for CGST',
    )
    transaction_type = models.BooleanField(
        choices=TRANSACTION_TYPE_CHOICES,
        default=TRANSACTION_INTRASTATE,
    )

    @property
    def total(self) -> float:
        total_tax = self.cgst + self.tax.sgst
        return round(
            (total_tax / 100) * (self.salary_income + self.share_market_income), 2
        )

    def save(self, *args, **kwargs):

        if self.id:
            # simple field editing, continue as normal
            super().save(*args, **kwargs)

        if self.tax.status == Tax.STATUS_PAID:
            raise ValidationError('Cannot edit paid taxes')

        # Check if there are any past dues for this tax
        if self.tax.history.count() > 0:
            self.tax.history.filter(active=True).update(active=False)

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.issued_on} - Rs. {self.total}'
