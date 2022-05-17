import json
import random
from datetime import timedelta

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from user.models import User
from tax.models import Tax, TaxDue
from tax.views import TaxListCreateAPIView
from fixtures.users import create_fake_user
from tax.serializers import TaxListSerializer
from fixtures.taxes.factory import create_fake_tax, create_fake_tax_serializer_data


# noinspection DuplicatedCode
class TaxCreateTests(APITestCase):

    fixtures = ['states/data.json']

    @classmethod
    def setUpTestData(cls):
        cls.taxpayer = create_fake_user()
        cls.admin = create_fake_user(role=User.ADMIN)

    def test_only_accountant_or_admin_can_issue_tax(self):

        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            reverse('tax:tax-list-create'),
            content_type='application/json',
            data=json.dumps(create_fake_tax_serializer_data(self.taxpayer)),
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tax.objects.count(), 1)
        self.assertEqual(TaxDue.objects.count(), 1)

        created_tax = Tax.objects.get()

        self.assertEqual(created_tax.payer, self.taxpayer)
        self.assertEqual(created_tax.sgst, self.taxpayer.info.state.tax)

        self.client.logout()

    def test_taxpayer_cannot_issue_tax(self):
        self.client.force_authenticate(user=self.taxpayer)

        response = self.client.post(
            reverse('tax:tax-list-create'),
            content_type='application/json',
            data=json.dumps(create_fake_tax_serializer_data(self.taxpayer)),
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Tax.objects.count(), 0)
        self.assertEqual(TaxDue.objects.count(), 0)

        self.client.logout()


# noinspection DuplicatedCode
class TaxUpdateTests(APITestCase):

    fixtures = ['states/data.json']

    @classmethod
    def setUpTestData(cls):
        cls.taxpayer = taxpayer = create_fake_user()
        cls.accountant = create_fake_user(User.TAXACCOUNTANT)

        cls.paid_tax = create_fake_tax(taxpayer, paid=True)
        cls.unpaid_tax = create_fake_tax(taxpayer, paid=False)

    def test_taxpayer_cannot_update_tax(self):
        self.client.force_login(user=self.taxpayer)

        response = self.client.patch(
            reverse('tax:tax-retrieve-update', kwargs={'pk': self.unpaid_tax.pk}),
            data={'due_date': str(self.unpaid_tax.due_date + timedelta(days=10))},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            Tax.objects.get(pk=self.unpaid_tax.pk).due_date, self.unpaid_tax.due_date
        )

        self.client.logout()

    def test_only_accountant_or_admin_can_update_tax(self):

        self.client.force_login(user=self.accountant)

        # say, a benevolent accountant postpones the due date by 10 days
        response = self.client.patch(
            reverse('tax:tax-retrieve-update', kwargs={'pk': self.unpaid_tax.pk}),
            data={'due_date': str(self.unpaid_tax.due_date + timedelta(days=10))},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(
            response.data['due_date'],
            str(self.unpaid_tax.due_date + timedelta(days=10)),
        )
        self.assertEqual(
            Tax.objects.get(pk=self.unpaid_tax.pk).due_date,
            self.unpaid_tax.due_date + timedelta(days=10),
        )
        self.client.logout()


# noinspection DuplicatedCode
class TaxListTests(APITestCase):

    fixtures = ['states/data.json']

    @classmethod
    def setUpTestData(cls):

        cls.taxpayer1 = create_fake_user()
        cls.taxpayer2 = create_fake_user()

        cls.admin = create_fake_user(User.ADMIN)
        cls.taxaccountant = create_fake_user(User.TAXACCOUNTANT)

        # noinspection PyUnresolvedReferences
        cls.taxpayer1_taxes = [
            create_fake_tax(cls.taxpayer1, paid=False)
            for _ in range(random.randint(2, 3))
        ]
        # noinspection PyUnresolvedReferences
        cls.taxpayer2_taxes = [
            create_fake_tax(cls.taxpayer2, paid=False)
            for _ in range(random.randint(2, 8))
        ]

    def test_admin_accountant_view_all_taxes(self):
        """
        Tests that admins and accountants can view all taxes.
        """

        request_factory = APIRequestFactory()

        for staff_member in [self.admin, self.taxaccountant]:

            self.client.force_login(staff_member)

            request = request_factory.get(reverse('tax:tax-list-create'))
            force_authenticate(request, user=staff_member)
            response = TaxListCreateAPIView.as_view()(request)

            response.render()
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response_data), Tax.objects.all().count())
            self.assertEqual(
                json.loads(response.content),
                TaxListSerializer(
                    Tax.objects.all().order_by('-pk'),
                    many=True,
                    context={'request': request},
                ).data,
            )

            self.client.logout()

    def test_taxpayer_only_views_own_taxes(self):
        """
        Tests that taxpayers can only view their own taxes.
        """

        request_factory = APIRequestFactory()

        for i, taxpayer in enumerate([self.taxpayer1, self.taxpayer2]):

            taxpayer_taxes: list[Tax] = getattr(self, f'taxpayer{i+1}_taxes')
            taxpayer_taxes.reverse()

            self.client.force_login(taxpayer)

            request = request_factory.get(reverse('tax:tax-list-create'))
            force_authenticate(request, user=taxpayer)
            response = TaxListCreateAPIView.as_view()(request)

            response.render()
            response_data = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response_data), len(taxpayer_taxes))
            self.assertEqual(
                response_data,
                TaxListSerializer(
                    taxpayer_taxes, many=True, context={'request': request}
                ).data,
            )

            self.client.logout()
