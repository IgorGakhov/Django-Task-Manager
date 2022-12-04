from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms import BaseForm
from typing import Dict, Any, Union, Callable, Type

from .models import Users
from .forms import UserRegistrationForm, UserEditingForm
from .constants import REVERSE_USERS, \
    CONTEXT_LIST, CONTEXT_CREATE, CONTEXT_UPDATE, CONTEXT_DELETE


class UsersListView(ListView):
    '''Show the list of users.'''
    model: Type[Users] = Users
    context_object_name: str = 'users'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''Sets additional meta information.'''
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update(CONTEXT_LIST)
        return context


class UserCreateView(CreateView):
    '''Create a user.'''
    model: Type[Users] = Users
    form_class: Type[BaseForm] = UserRegistrationForm
    success_url: Union[str, Callable[..., Any]] = REVERSE_USERS

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''Sets additional meta information and a button.'''
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update(CONTEXT_CREATE)
        return context


class UserUpdateView(UpdateView):
    '''Change a user.'''
    model: Type[Users] = Users
    form_class: Type[BaseForm] = UserEditingForm
    success_url: Union[str, Callable[..., Any]] = REVERSE_USERS

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''Sets additional meta information and a button.'''
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update(CONTEXT_UPDATE)
        return context


class UserDeleteView(DeleteView):
    '''Delete a user.'''
    model: Type[Users] = Users
    context_object_name: str = 'user'
    success_url: Union[str, Callable[..., Any]] = REVERSE_USERS

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''Sets additional meta information and a button.'''
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update(CONTEXT_DELETE)
        return context
