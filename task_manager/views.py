from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin

from .constants import HOME, MSG_LOGIN, MSG_LOGOUT, TEMPLATE_INDEX


class HomePageView(TemplateView):
    "Main page."
    template_name: str = TEMPLATE_INDEX


class UserLoginView(SuccessMessageMixin, LoginView):
    "Log in into Task Manager."
    next_page: str = HOME
    success_message = MSG_LOGIN


class UserLogoutView(SuccessMessageMixin, LogoutView):
    "Log out from Task Manager."
    next_page: str = HOME
    success_message = MSG_LOGOUT
