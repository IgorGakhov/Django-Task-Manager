from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView


class HomePageView(TemplateView):
    "Main page."
    template_name: str = 'index.html'


class UserLoginView(LoginView):
    "Log in into Task Manager."
    next_page: str = 'home'


class UserLogoutView(LogoutView):
    "Log out from Task Manager."
    next_page: str = 'home'
