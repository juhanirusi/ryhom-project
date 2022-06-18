#from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import RegisterUserForm


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterUserForm
    #success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    success_url = 'index.html'
