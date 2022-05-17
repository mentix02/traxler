import random
from typing import Union
from datetime import date

from django.utils import timezone

from user.models import User
from tax.models import Tax, TaxDue


def create_fake_tax_serializer_data(
    payer: User,
    due_date: date = None,
) -> dict[str, Union[str, int, bool]]:

    if not due_date:
        due_date = timezone.now().date() + timezone.timedelta(
            days=random.randint(1, 30)
        )

    return dict(
        payer=payer.id,
        due_date=str(due_date),
        active_due=dict(
            cgst=random.randint(4, 35),
            transaction_type=random.random() > 0.5,
            salary_income=random.randint(10000, 100000),
            share_market_income=random.randint(1000, 20000),
        ),
    )


def create_fake_tax(
    payer: User,
    paid: bool = False,
    due_date: date = None,
) -> Tax:

    if not due_date:
        due_date = timezone.now().date() + timezone.timedelta(
            days=random.randint(1, 30)
        )

    tax = Tax.objects.create(
        payer=payer,
        due_date=due_date,
        sgst=payer.info.state.tax,
    )

    TaxDue.objects.create(
        tax=tax,
        cgst=random.randint(4, 35),
        transaction_type=random.random() > 0.5,
        salary_income=random.randint(10000, 100000),
        share_market_income=random.randint(1000, 20000),
    )

    # Have to set `paid` after creating TaxDue since
    # TaxDue's save raises an exception if we try to
    # edit a tax after it's been paid.
    tax.paid = paid
    tax.save()

    return tax
