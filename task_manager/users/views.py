from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.forms import BaseForm
from django.http import HttpResponse, HttpRequest
from django.db.models import ProtectedError
from typing import Dict, Any, Union, Callable, Type

from .models import User
from .forms import UserRegistrationForm, UserEditingForm
from .constants import REVERSE_USERS, REVERSE_LOGIN, \
    CONTEXT_LIST, CONTEXT_CREATE, CONTEXT_UPDATE, CONTEXT_DELETE, \
    MSG_REGISTERED, MSG_UPDATED, MSG_DELETED, MSG_UNPERMISSION_TO_MODIFY, \
    USER_USED_IN_TASK


class UsersListView(ListView):
    '''Show the list of users.'''
    model: Type[User] = User
    context_object_name: str = 'users'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''Sets additional meta information.'''
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update(CONTEXT_LIST)
        return context


class UserCreateView(SuccessMessageMixin, CreateView):
    '''Create a user.'''
    model: Type[User] = User
    form_class: Type[BaseForm] = UserRegistrationForm
    success_url: Union[str, Callable[..., Any]] = REVERSE_LOGIN
    success_message: str = MSG_REGISTERED

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''Sets additional meta information and a button.'''
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update(CONTEXT_CREATE)
        return context


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    '''Change a user.'''
    model: Type[User] = User
    form_class: Type[BaseForm] = UserEditingForm
    success_url: Union[str, Callable[..., Any]] = REVERSE_USERS
    success_message: str = MSG_UPDATED

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''Sets additional meta information and a button.'''
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update(CONTEXT_UPDATE)
        return context

    def dispatch(self, request: HttpRequest,
                 *args: Any, **kwargs: Any) -> HttpResponse:
        '''Specifies access settings for the current user.
        Provides access if the user is authenticated.'''
        if request.user.id != self.get_object().id:
            messages.error(self.request, MSG_UNPERMISSION_TO_MODIFY)
            return redirect(REVERSE_USERS)
        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    '''Delete a user.'''
    model: Type[User] = User
    context_object_name: str = 'user'
    success_url: Union[str, Callable[..., Any]] = REVERSE_USERS
    success_message: str = MSG_DELETED

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        '''Sends data to the server with protection check.'''
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, USER_USED_IN_TASK)
            return redirect(REVERSE_USERS)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''Sets additional meta information and a button.'''
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update(CONTEXT_DELETE)
        return context

    def dispatch(self, request: HttpRequest,
                 *args: Any, **kwargs: Any) -> HttpResponse:
        '''Specifies access settings for the current user.
        Provides access if the user is authenticated.'''
        if request.user.id != self.get_object().id:
            messages.error(self.request, MSG_UNPERMISSION_TO_MODIFY)
            return redirect(REVERSE_USERS)
        return super().dispatch(request, *args, **kwargs)
