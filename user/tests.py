import random

from django.urls import reverse
from django.test import TestCase

from rest_framework import status

from user.models import User
from fixtures.users import create_fake_user
from fixtures.users.factory import DEFAULT_PASSWORD


class ObtainAuthTokenAPIViewTest(TestCase):

    fixtures = ['states/data.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = create_fake_user()

    def test_obtain_auth_token_success(self):

        response = self.client.post(
            reverse('user:token'),
            {'password': DEFAULT_PASSWORD, 'username': self.user.username},
        )

        # noinspection PyUnresolvedReferences
        expected_data = {
            'role': self.user.role,
            'username': self.user.username,
            'token': self.user.auth_token.key,
        }

        self.assertEqual(expected_data, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ListTaxpayersTest(TestCase):

    fixtures = ['states/data.json']

    @classmethod
    def setUpTestData(cls):
        admin = create_fake_user()

        admin.is_staff = True
        admin.role = User.ADMIN
        admin.is_superuser = True
        admin.save()
        cls.admin = admin

        accountant = create_fake_user()
        accountant.role = User.TAXACCOUNTANT
        accountant.save()
        cls.accountant = accountant

        cls.taxpayers = [create_fake_user() for _ in range(3)]

    def test_list_taxpayers_as_admin(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('user:taxpayer-list-create'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_list_taxpayers_as_accountant(self):
        self.client.force_login(self.accountant)
        response = self.client.get(reverse('user:taxpayer-list-create'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_list_taxpayers_unauthorized(self):
        response = self.client.get(reverse('user:taxpayer-list-create'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_taxpayers_as_taxpayer(self):
        self.client.force_login(random.choice(self.taxpayers))
        response = self.client.get(reverse('user:taxpayer-list-create'))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()
