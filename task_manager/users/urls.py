from django.urls import path, URLPattern
from typing import List

from .views import UsersListView, UserCreateView, UserUpdateView, UserDeleteView


urlpatterns: List[URLPattern] = [
    path('', UsersListView.as_view(), name='users'),
    path('create/', UserCreateView.as_view(), name='sign_up'),
    path('<pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<pk>/delete/', UserDeleteView.as_view(), name='user_delete')
]
