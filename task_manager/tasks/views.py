from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.forms.forms import BaseForm
from django.http import HttpResponse, HttpResponseRedirect
from typing import Dict, Any, Tuple, Union, Callable, Type

from .models import Task, User
from .constants import REVERSE_TASKS, REVERSE_LOGIN, \
    CONTEXT_LIST, CONTEXT_CREATE, CONTEXT_UPDATE, CONTEXT_DELETE, CONTEXT_DETAIL, \
    MSG_CREATED, MSG_UPDATED, MSG_DELETED, MSG_NO_PERMISSION, \
    MSG_NOT_AUTHOR_FOR_DELETE_TASK, NAME, STATUS, DESCRIPTION, EXECUTOR, LABELS


class TasksListView(LoginRequiredMixin, ListView):
    '''Show the list of tasks.'''
    model: Type[Task] = Task
    context_object_name: str = 'tasks'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''Sets additional meta information.'''
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update(CONTEXT_LIST)
        return context

    def handle_no_permission(self) -> HttpResponseRedirect:
        '''Sets rules when a page is unavailable to an unauthorized user.'''
        messages.warning(self.request, MSG_NO_PERMISSION)
        return redirect(REVERSE_LOGIN)


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    '''Create a task.'''
    model: Type[Task] = Task
    fields: Tuple = (NAME, STATUS, DESCRIPTION, EXECUTOR, LABELS)
    success_url: Union[str, Callable[..., Any]] = REVERSE_TASKS
    success_message: str = MSG_CREATED

    def form_valid(self, form: BaseForm) -> HttpResponse:
        '''Sets the author of the task by the ID of the current user.'''
        user: User = self.request.user
        form.instance.author: BaseForm[User] = User.objects.get(id=user.id)
        return super(TaskCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''Sets additional meta information and a button.'''
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update(CONTEXT_CREATE)
        return context

    def handle_no_permission(self) -> HttpResponseRedirect:
        '''Sets rules when a page is unavailable to an unauthorized user.'''
        messages.warning(self.request, MSG_NO_PERMISSION)
        return redirect(REVERSE_LOGIN)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    '''Change a task.'''
    model: Type[Task] = Task
    fields: Tuple = (NAME, STATUS, DESCRIPTION, EXECUTOR, LABELS)
    success_url: Union[str, Callable[..., Any]] = REVERSE_TASKS
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


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    '''Delete a task.'''
    model: Type[Task] = Task
    context_object_name: str = 'task'
    success_url: Union[str, Callable[..., Any]] = REVERSE_TASKS
    success_message: str = MSG_DELETED

    def dispatch(self, request, *args, **kwargs):
        '''Specifies access settings for the current user.
        Provides access if the user is authenticated.'''
        if request.user.id != self.get_object().author.id:
            if request.user.is_authenticated:
                messages.error(self.request, MSG_NOT_AUTHOR_FOR_DELETE_TASK)
            return redirect(REVERSE_TASKS)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''Sets additional meta information and a button.'''
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update(CONTEXT_DELETE)
        return context

    def handle_no_permission(self) -> HttpResponseRedirect:
        '''Sets rules when a page is unavailable to an unauthorized user.'''
        messages.warning(self.request, MSG_NO_PERMISSION)
        return redirect(REVERSE_LOGIN)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model: Type[Task] = Task

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        '''Sets additional meta information and a button.'''
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context.update(CONTEXT_DETAIL)
        return context

    def handle_no_permission(self) -> HttpResponseRedirect:
        '''Sets rules when a page is unavailable to an unauthorized user.'''
        messages.warning(self.request, MSG_NO_PERMISSION)
        return redirect(REVERSE_LOGIN)
