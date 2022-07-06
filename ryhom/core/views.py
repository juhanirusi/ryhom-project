from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
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


@login_required
def user_profile_redirect(request):
    """
    Used as a dynamic redirect to user's personal profile, because the
    user profile URL requires a slug kwarg, hence, a custom redirect

    settings.py --> LOGIN_REDIRECT_URL
    """
    slug = request.user.slug
    return redirect('accounts:user_profile', user_profile_slug=slug)
