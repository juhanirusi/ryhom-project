from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect


class RedirectAuthenticatedUserMixin(UserPassesTestMixin):
    redirect_to = settings.LOGIN_REDIRECT_URL

    def handle_no_permission(self):
        return HttpResponseRedirect(self.redirect_to)

    def test_func(self):
        if self.request.user.is_authenticated:
            return False
        return True
