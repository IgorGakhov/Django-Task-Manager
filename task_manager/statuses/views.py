from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.db.models import ProtectedError
from typing import Dict, Any, Tuple, Union, Callable, Type

from .models import Status
from .constants import REVERSE_LOGIN, REVERSE_STATUSES, NAME, \
    CONTEXT_LIST, CONTEXT_CREATE, CONTEXT_UPDATE, CONTEXT_DELETE, \
    MSG_CREATED, MSG_UPDATED, MSG_DELETED, MSG_NO_PERMISSION, STATUS_USED_IN_TASK


class StatusesListView(LoginRequiredMixin, ListView):
    '''Show the list of statuses.'''
    model: Type[Status] = Status
    context_object_name: str = 'statuses'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''Sets additional meta information.'''
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update(CONTEXT_LIST)
        return context

    def handle_no_permission(self) -> HttpResponseRedirect:
        '''Sets rules when a page is unavailable to an unauthorized user.'''
        messages.warning(self.request, MSG_NO_PERMISSION)
        return redirect(REVERSE_LOGIN)


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

    def handle_no_permission(self) -> HttpResponseRedirect:
        '''Sets rules when a page is unavailable to an unauthorized user.'''
        messages.warning(self.request, MSG_NO_PERMISSION)
        return redirect(REVERSE_LOGIN)


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

    def handle_no_permission(self) -> HttpResponseRedirect:
        '''Sets rules when a page is unavailable to an unauthorized user.'''
        messages.warning(self.request, MSG_NO_PERMISSION)
        return redirect(REVERSE_LOGIN)


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    '''Delete a status.'''
    model: Type[Status] = Status
    context_object_name: str = 'status'
    success_url: Union[str, Callable[..., Any]] = REVERSE_STATUSES
    success_message: str = MSG_DELETED

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        '''Sends data to the server with protection check.'''
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, STATUS_USED_IN_TASK)
            return redirect(REVERSE_STATUSES)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''Sets additional meta information and a button.'''
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update(CONTEXT_DELETE)
        return context

    def handle_no_permission(self) -> HttpResponseRedirect:
        '''Sets rules when a page is unavailable to an unauthorized user.'''
        messages.warning(self.request, MSG_NO_PERMISSION)
        return redirect(REVERSE_LOGIN)
