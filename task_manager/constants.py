"Constants for Task Manager main application."

from django.utils.translation import gettext_lazy
from typing import Final


# Route names
HOME: Final[str] = 'home'
LOGIN: Final[str] = 'login'
LOGOUT: Final[str] = 'logout'


# Messages
MSG_LOGIN: str = gettext_lazy('You are logged in')
MSG_LOGOUT: str = gettext_lazy('Logged out successfully')


# Templates
TEMPLATE_INDEX: Final[str] = 'index.html'
