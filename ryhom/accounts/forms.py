from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import Account


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['name'].widget.attrs['placeholder'] = 'First and last name'
        self.fields['password1'].widget.attrs['placeholder'] = '********'
        self.fields['password2'].widget.attrs['placeholder'] = '********'

        self.fields['password1'].label = 'Pick a Password'
        self.fields['password2'].label = 'Re-enter Password'

        for fieldname in ['email', 'name', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['password1'].help_text = 'Your password must contain at least 8 characters.'

    class Meta:
        model = Account
        fields = ('email', 'name', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    """
    Our custom login form that subclasses Django's AuthenticationForm,
    but also includes our custom placeholders, labels and an error
    message for users who haven't verified their email address.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Enter email or username'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter password'

        self.fields['username'].label = 'Email or username'

    class Meta:
        model = Account
        fields = ('email', 'password')


    def confirm_login_allowed(self, user):
        """
        Let users who haven't clicked their email verification
        link know that they can't log into their account until
        verifying the account.
        """
        if not user.is_active:
            raise ValidationError('Your account is still inactive! \
                Click the confirmation link sent to your email to \
                activate it.',
                code='mycode'
            )
