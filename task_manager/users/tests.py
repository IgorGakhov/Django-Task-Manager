from django.test import TestCase
from django.http import HttpResponse

from .constants import REVERSE_USERS


class UsersTest(TestCase):

    def test_users_list(self) -> None:
        response: HttpResponse = self.client.get(REVERSE_USERS)
        self.assertTemplateUsed(response, template_name='users/users_list.html')
        self.assertEqual(response.status_code, 200)
