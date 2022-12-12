from django.test import TestCase, Client
from django.contrib.auth import SESSION_KEY
from django.urls import reverse_lazy
from django.http import HttpResponse

from http import HTTPStatus
from typing import Dict

from task_manager.users.models import Users
from task_manager.constants import HOME, TEMPLATE_INDEX, \
    REVERSE_HOME, REVERSE_LOGIN, REVERSE_LOGOUT
from task_manager.users.constants import UPDATE_USER, DELETE_USER


class HomePageTest(TestCase):

    fixtures = ['users.json']

    def test_user_update_view(self) -> None:
        ROUTE = reverse_lazy(HOME)

        response: HttpResponse = self.client.get(ROUTE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name=TEMPLATE_INDEX)


class AuthenticationTest(TestCase):

    fixtures = ['users.json']

    def setUp(self) -> None:
        self.client: Client = Client()
        self.credentials: Dict[str, str] = {
            'username': 'testuser',
            'password': 'secret_password'
        }
        self.user: Users = Users.objects.create_user(**self.credentials)

    def test_login(self) -> None:
        # Send login data and checking if a redirect exists
        response: HttpResponse = self.client.post(
            REVERSE_LOGIN, self.credentials, follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, REVERSE_HOME)
        # Should be logged in now
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self) -> None:
        # Log in and make sure the session is valid
        self.client.login(**self.credentials)
        self.assertTrue(SESSION_KEY in self.client.session)
        # There should be no session key on exit
        response: HttpResponse = self.client.get(REVERSE_LOGOUT)
        self.assertTrue(SESSION_KEY not in self.client.session)
        # Checking if a redirect exists
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_HOME)

    def test_inaccessibility_of_pages_by_auth(self) -> None:
        accessible_id: int = 1
        self.client.force_login(Users.objects.get(pk=accessible_id))

        inaccessible_id: int = 2
        for route_name in (UPDATE_USER, DELETE_USER):
            response: HttpResponse = self.client.get(
                reverse_lazy(route_name, args=[inaccessible_id])
            )
            self.assertEqual(response.status_code, HTTPStatus.FOUND)
