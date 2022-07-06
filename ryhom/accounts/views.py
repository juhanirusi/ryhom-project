import socket
from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import DetailView, View
from django.views.generic.edit import CreateView, UpdateView
from ryhom.articles.models import Article, Comment
from ryhom.core.decorators import confirm_password
from ryhom.core.viewmixins import RedirectAuthenticatedUserMixin

from .forms import (AccountSettingsForm, ChangeEmailForm, ChangePasswordForm,
                    ForgotPasswordForm, LoginForm, RegisterForm,
                    SetNewPasswordForm)
from .models import Account
from .tokens import account_token_generator
from .utils import send_registration_confirm_email

# A list of decorators including our custom decorator -> confirm_password
# that requires the user to insert their password again if there's more
# than, 30 minutes for example, from their last login if they are
# accessing a view with this decorator.
decorators = [login_required, confirm_password]


class RegisterView(RedirectAuthenticatedUserMixin, CreateView):
    form_class = RegisterForm
    template_name = 'accounts/create-account.html'
    success_url = reverse_lazy('accounts:create_account')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False # Deactivate account till it is confirmed
        user.save()

        to_email = form.cleaned_data['email']

        # For all possible send_mail (SMTPException) exceptions...
        # https://docs.python.org/3/library/smtplib.html#smtplib.SMTPException
        try:
            send_registration_confirm_email(self, user, to_email)
            success_message = (f'An account has been created! We\'ve sent \
                                a verification link to <b>{to_email}</b>. \
                                Click it to activate your account!')
            messages.success(self.request, success_message)
        except (SMTPException, socket.gaierror):
            error_message = 'There was an error connecting to the email \
                            server, this is likely our fault. Please try \
                            creating an account later.'
            messages.error(self.request, error_message)

        return super().form_valid(form)


    def form_invalid(self, form):
        error_message = (
            'Error creating the user, please fix the errors below...'
        )
        messages.error(self.request, error_message)
        return super().form_invalid(form)


class ActivateAccountView(View):
    def get(self, request, uidb64, token,
            backend='django.contrib.auth.backends.ModelBackend'):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except (TypeError,
                ValueError,
                OverflowError,
                Account.DoesNotExist):

            user = None

        if user is not None and account_token_generator.check_token(
            user, token):

            user.is_active = True
            user.save()

            if request.user.is_authenticated:
                logout(request)

            login(
                request,
                user,
                backend
            )
            messages.success(request, 'Your email address has been verfied!')
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.warning(request, ('The confirmation link was invalid, \
                                possibly because it has already been used.'))
            return redirect(settings.LOGIN_URL)


class LoginUserView(LoginView):
    authentication_form = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = settings.LOGIN_REDIRECT_URL


class LogoutUserView(LogoutView):
    def get_next_page(self):
        next_page = super(LogoutUserView, self).get_next_page()
        messages.add_message(
            self.request, messages.SUCCESS,
            "You've successfully logged out!"
        )
        return next_page


@method_decorator(decorators, name='dispatch')
class AccountSettingsView(UpdateView):
    template_name = 'accounts/account-settings.html'
    form_class = AccountSettingsForm
    success_url = reverse_lazy('accounts:account_settings')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request,
            'Your changes were successfully saved!'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,
                    'Unable to make the changes, \
                    fix the errors below and try again.'
        )
        return self.render_to_response(self.get_context_data(form=form))


class UserProfileView(DetailView):
    model = Account
    template_name = 'accounts/user-profile.html'

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['book_list'] = Book.objects.all()
    #     return context

    def get_object(self):
        self.user = get_object_or_404(Account, slug=self.kwargs['user_profile_slug'])
        print(self.user)
        return self.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_posts = Article.user_posts.user_profile_published(self.user)
        user_comments = Comment.user_comments.user_profile_comments(self.user)
        context['user_posts'] = user_posts
        context['user_comments'] = user_comments

        return context


@method_decorator(decorators, name='dispatch')
class ChangePasswordView(PasswordChangeView):
    template_name = 'accounts/change-password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('accounts:account_settings')

    def form_valid(self, form):
        messages.success(self.request,
            'Your password was changed successfully!'
        )
        # Updating the password logs out all other sessions
        # for the user except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        error_message = 'We couldn\'t change your password, \
                        fix the errors below and try again.'

        messages.error(self.request, error_message)
        return self.render_to_response(self.get_context_data(form=form))


# PASSWORD RESET START ---------------------------------------------------

class ResetPasswordView(RedirectAuthenticatedUserMixin, PasswordResetView):
    template_name = 'accounts/password-reset.html'
    email_template_name = 'accounts/password-reset-email.html'
    form_class = ForgotPasswordForm
    from_email = 'noreply@ryhom.com'
    success_url = reverse_lazy('accounts:password_reset_message')


class ResetPasswordMessageView(PasswordResetDoneView):
    template_name = 'accounts/password-reset-done.html'


class ResetPasswordConfirmationView(PasswordResetConfirmView):
    template_name = 'accounts/password-reset-confirm.html'
    form_class = SetNewPasswordForm
    success_url = reverse_lazy('accounts:password_reset_done')


class ResetPasswordDoneView(PasswordResetCompleteView):
    template_name = 'accounts/password-reset-complete.html'

# PASSWORD RESET END -----------------------------------------------------


@method_decorator(decorators, name='dispatch')
class ChangeEmailView(UpdateView):
    template_name = 'accounts/change-email.html'
    form_class = ChangeEmailForm
    success_url = reverse_lazy('accounts:account_settings')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        new_email = form.cleaned_data['new_email']
        self.request.user.email = new_email

        success_message = f'Changing your email was successful! \
                            You can now login into your account \
                            with <b>{new_email}</b>.'

        messages.success(self.request, success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        error_message = 'We couldn\'t change your email address, \
                        fix the errors below and try again.'

        messages.error(self.request, error_message)
        return self.render_to_response(self.get_context_data(form=form))
