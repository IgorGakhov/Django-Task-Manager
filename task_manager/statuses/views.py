from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from typing import Dict, Any, Tuple, Union, Callable, Type

from .models import Status
from .constants import REVERSE_STATUSES, NAME, \
    CONTEXT_LIST, CONTEXT_CREATE, CONTEXT_UPDATE, CONTEXT_DELETE, \
    MSG_CREATED, MSG_UPDATED, MSG_DELETED


class StatusesListView(LoginRequiredMixin, ListView):
    '''Show the list of statuses.'''
    model: Type[Status] = Status
    context_object_name: str = 'statuses'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''Sets additional meta information.'''
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update(CONTEXT_LIST)
        return context


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    '''Create a status.'''
    model: Type[Status] = Status
    fields: Tuple = (NAME,)
    success_url: Union[str, Callable[..., Any]] = REVERSE_STATUSES
    success_message: str = MSG_CREATED

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''Sets additional meta information and a button.'''
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update(CONTEXT_CREATE)
        return context


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    '''Change a status.'''
    model: Type[Status] = Status
    fields: Tuple = (NAME,)
    success_url: Union[str, Callable[..., Any]] = REVERSE_STATUSES
    success_message: str = MSG_UPDATED

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''Sets additional meta information and a button.'''
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update(CONTEXT_UPDATE)
        return context


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    '''Delete a status.'''
    model: Type[Status] = Status
    context_object_name: str = 'status'
    success_url: Union[str, Callable[..., Any]] = REVERSE_STATUSES
    success_message: str = MSG_DELETED

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''Sets additional meta information and a button.'''
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update(CONTEXT_DELETE)
        return context
