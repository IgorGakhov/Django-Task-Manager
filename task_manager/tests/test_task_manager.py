from django.test import TestCase, Client
from django.contrib.auth import SESSION_KEY
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.http import HttpResponse

from http import HTTPStatus
from dataclasses import dataclass
from typing import Dict, Tuple

from task_manager.users.models import User
from task_manager.constants import HOME, TEMPLATE_INDEX, \
    REVERSE_HOME, REVERSE_LOGIN, REVERSE_LOGOUT, NO_PERMISSION_MESSAGE
from task_manager.users.constants import UPDATE_USER, DELETE_USER
from task_manager.statuses.constants import \
    LIST_STATUSES, CREATE_STATUS, UPDATE_STATUS, DELETE_STATUS


class HomePageTest(TestCase):

    fixtures = ['user.json']

    def test_user_update_view(self) -> None:
        ROUTE = reverse_lazy(HOME)

        response: HttpResponse = self.client.get(ROUTE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name=TEMPLATE_INDEX)


class AuthenticationTest(TestCase):

    fixtures = ['user.json']

    def setUp(self) -> None:
        self.client: Client = Client()
        self.credentials: Dict[str, str] = {
            'username': 'testuser',
            'password': 'secret_password'
        }
        self.user: User = User.objects.create_user(**self.credentials)

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

        @dataclass
        class NotAllowedPageRoutes:
            with_pk: Tuple = (UPDATE_STATUS, DELETE_STATUS)
            without_pk: Tuple = (LIST_STATUSES, CREATE_STATUS)
            _all: Tuple = with_pk + without_pk

        # Test for inaccessibility of pages for an unauthorized user
        for not_allowed_page_route in NotAllowedPageRoutes._all:
            if not_allowed_page_route in NotAllowedPageRoutes.with_pk:
                response: HttpResponse = self.client.get(
                    reverse_lazy(not_allowed_page_route, args=[1])
                )
            else:
                response: HttpResponse = self.client.get(
                    reverse_lazy(not_allowed_page_route)
                )
            self.assertEqual(response.status_code, HTTPStatus.FOUND)
            self.assertRedirects(response, REVERSE_LOGIN)
            self.assertRaisesMessage(
                expected_exception=PermissionDenied,
                expected_message=NO_PERMISSION_MESSAGE
            )

        # Test for prohibition of changing user information by another user
        accessible_id: int = 1
        self.client.force_login(User.objects.get(pk=accessible_id))

        inaccessible_id: int = 2
        for route in (UPDATE_USER, DELETE_USER):
            response: HttpResponse = self.client.get(
                reverse_lazy(route, args=[inaccessible_id])
            )
            self.assertEqual(response.status_code, HTTPStatus.FOUND)
