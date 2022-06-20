#from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import View
from django.views.generic.edit import CreateView

from .forms import RegisterUserForm
from .models import UserProfile
from .utils import account_activation_token


class RegisterView(CreateView):

    template_name = 'accounts/create-account.html'
    form_class = RegisterUserForm
    #success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    success_url =  reverse_lazy('create-account')


    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False # Deactivate account till it is confirmed
        user.save()

        # To get the domain of the current site
        current_site = get_current_site(self.request)

        mail_subject = 'Welcome To Ryhom.com! Just One More Step...'
        message = render_to_string('accounts/verification-email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        to_email = form.cleaned_data['email']
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()

        success_message = f"An account has been created! \
                We've sent a verification link to <b>{to_email}</b>. \
                Click it to activate your account!"

        messages.success(self.request, success_message)
        return super().form_valid(form)


    def form_invalid(self, form):
        error_message = 'Error creating the user, please fix the errors below...'
        messages.error(self.request, error_message)
        return super().form_invalid(form)


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserProfile.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'GREAT! NOW LOGIN!')
            return redirect('accounts/create-account.html')
        else:
            messages.warning(request, ('The confirmation link was invalid, \
                                possibly because it has already been used.'))
            return redirect('accounts/create-account.html')


def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.success(request, ('Antamasi salasana tai käyttäjätunnus on väärä!'))
            return redirect('accounts/login.html')
    else:
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'accounts/login.html')
