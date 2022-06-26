from django.http import Http404
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

from .forms import ConfirmPasswordForm


class IndexView(TemplateView):
    template_name = 'index.html'


class ConfirmPasswordView(UpdateView):
    form_class = ConfirmPasswordForm
    template_name = 'continue-session.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return self.request.get_full_path()


class Error404View(View):
    def index(self):
        raise Http404
