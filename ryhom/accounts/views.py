from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
#from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import View
from django.views.generic.edit import CreateView

from .forms import LoginForm, RegisterForm
from .models import Account
from .utils import account_token_generator


class RegisterView(CreateView):

    template_name = 'accounts/create-account.html'
    form_class = RegisterForm
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
            'token': account_token_generator.make_token(user),
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
            messages.success(request, 'Email verfied!')
            # CHANGE TO PROFILE PAGE IN THE FUTURE!
            return redirect('index')
        else:
            messages.warning(request, ('The confirmation link was invalid, \
                                possibly because it has already been used.'))
            return redirect('index')


# def login_user(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('index')
#         else:
#             messages.success(request, ('Antamasi salasana tai käyttäjätunnus on väärä!'))
#             return redirect('login')
#     else:
#         if request.user.is_authenticated:
#             return redirect('index')
#         return render(request, 'accounts/login.html')







class LoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    next_page = 'index' # CHANGE IN THE FUTURE!
    redirect_authenticated_user = 'index' # CHANGE IN THE FUTURE!

    # def form_invalid(self, form):
    #     """If the form is invalid, render the invalid form."""
    #     return self.render_to_response(self.get_context_data(form=form))

    # def get(self, request):
    #     form = self.form_class
    #     messages.success(request, 'JEEEEEE!')
    #     return render(request, self.template_name, context={'form': form})

    # def post(self, request):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         user = authenticate(
    #             email=form.cleaned_data['email'],
    #             password=form.cleaned_data['password'],
    #         )
    #         if user is not None:
    #             login(request, user)
    #             return redirect('index')
    #     message = 'Login failed!'
    #     return render(request, self.template_name, context={'form': form, 'message': message})
