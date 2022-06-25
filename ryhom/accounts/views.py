from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeView,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import DetailView, View
from django.views.generic.edit import CreateView, UpdateView
from ryhom.core.viewmixins import RedirectAuthenticatedUserMixin

from .forms import (AccountSettingsForm, ChangeEmailForm, ChangePasswordForm,
                    ForgotPasswordForm, LoginForm, RegisterForm)
from .models import Account
from .tokens import account_token_generator


# ADD 'try/except' FUNCTIONALITY TO MOST OF THE VIEWS TO MAKE THEM BULLETPROOF
class RegisterView(RedirectAuthenticatedUserMixin, CreateView):
    form_class = RegisterForm
    template_name = 'accounts/create-account.html'
    success_url =  reverse_lazy('accounts:create_account')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False # Deactivate account till it is confirmed
        user.save()

        # Get the domain of the current site
        current_site = get_current_site(self.request)

        mail_subject = 'Welcome To Ryhom.com! Just One More Step...'
        message = render_to_string(
            'accounts/account-verification-email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_token_generator.make_token(user),
        })

        to_email = form.cleaned_data['email']
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()

        success_message = f"An account has been created! We've sent \
                            a verification link to <b>{to_email}</b>. \
                            Click it to activate your account!"

        messages.success(self.request, success_message)
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
            return redirect(settings.LOGIN_REDIRECT_URL) # PERHAPS SHOULD CHANGE THIS IN THE FUTURE


class LoginUserView(LoginView):
    authentication_form = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = settings.LOGIN_REDIRECT_URL


@login_required
def user_profile_redirect(request):
    """
    Used as a dynamic redirect to user's personal profile, because the
    user profile URL requires a slug kwarg, hence, a custom redirect

    settings.py --> LOGIN_REDIRECT_URL
    """
    slug = request.user.slug
    return redirect('accounts:user_profile', slug=slug)


class LogoutUserView(LogoutView):
    def get_next_page(self):
        next_page = super(LogoutUserView, self).get_next_page()
        messages.add_message(
            self.request, messages.SUCCESS,
            "You've successfully logged out!"
        )
        return next_page


class AccountSettingsView(LoginRequiredMixin, UpdateView):
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
                    "Unable to make the changes, \
                    fix the errors below and try again."
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

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the user posts
    #     user_posts = MyPost.objects.filter(author=self.request.user).order_by('-cr_date')
    #     context['user_posts'] = user_posts
    #     context['user'] = self.request.user
    #     return context


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
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
        error_message = "We couldn't change your password, \
                        fix the errors below and try again."

        messages.error(self.request, error_message)
        return self.render_to_response(self.get_context_data(form=form))


# KESKEN--------------------------------------------------------


class ResetPasswordView(RedirectAuthenticatedUserMixin, PasswordResetView):
    template_name = 'accounts/password-reset.html'
    email_template_name = 'accounts/password-reset-email.html'
    form_class = ForgotPasswordForm
    #from_email = None
    #html_email_template_name = None
    #subject_template_name = 'registration/password_reset_subject.txt'
    #success_url = reverse_lazy('password_reset_done')
    #token_generator = <django.contrib.auth.tokens.PasswordResetTokenGenerator object at 0x7fc0f7867ac0>


class ResetPasswordConfirmation(PasswordResetConfirmView):
    template_name = 'accounts/password-reset-confirm.html'


# KESKEN ---------------------------------------------


class ChangeEmailView(LoginRequiredMixin, UpdateView):
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
        error_message = "We couldn't change your email address, \
                        fix the errors below and try again."

        messages.error(self.request, error_message)
        return self.render_to_response(self.get_context_data(form=form))
