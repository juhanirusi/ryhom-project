from datetime import date

from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.core.exceptions import ValidationError
from django.forms import SelectDateWidget, Textarea
from django.utils.translation import gettext_lazy as _

from .models import Account


class RegisterForm(UserCreationForm):
    """
    Our custom registration form that subclasses Django's
    UserCreationForm, but also includes our custom
    placeholders, labels and help texts.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['name'].widget.attrs[
            'placeholder'
        ] = 'First and last name'
        self.fields['password1'].widget.attrs['placeholder'] = '********'
        self.fields['password2'].widget.attrs['placeholder'] = '********'

        self.fields['password1'].label = 'Pick a Password'
        self.fields['password2'].label = 'Re-enter Password'

        for fieldname in ['email', 'name', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['password1'].help_text = 'Password must contain at least 8 characters.'

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
                code='inactive'
            )


class AccountSettingsForm(UserChangeForm):
    """
    Our custom account settings form that subclasses Django's UserChangeForm,
    but also includes our custom placeholders, labels and a clean method to
    make sure that user's can't submit username's shorter than 3 characters.

    The birthday field has also been edited, so that user's can only choose
    reasonable years, for example user's can't be 200 or 1 year olds.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs[
            'placeholder'
        ] = 'First and last name'
        self.fields['bio'].widget.attrs['placeholder'] = 'Eat, sleep, garden.'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'

    password = None

    class Meta:
        model = Account
        fields = ('name', 'username', 'email', 'gender',
                'birthday', 'profile_image', 'bio',
        )

        labels = {
            'name'              : 'Full Name',
            'bio'               : 'Short Bio',
            'profile_image'     : 'Profile Image',
        }

        date_labels = ('Year', 'Month', 'Day')
        MONTHS = {
            1:_('Jan'), 2:_('Feb'), 3:_('Mar'), 4:_('Apr'),
            5:_('May'), 6:_('Jun'), 7:_('Jul'), 8:_('Aug'),
            9:_('Sep'), 10:_('Oct'), 11:_('Nov'), 12:_('Dec')
        }
        this_year = date.today().year
        year_range = [_ for _ in range(this_year - 100, this_year - 15)]

        widgets = {
            'birthday': SelectDateWidget(
                empty_label=date_labels,
                months=MONTHS,
                years=year_range
            ),
            'bio': Textarea(attrs={"rows":5, "cols":35})
        }

    def clean_username(self):
        """
        Validate the username field to ensure that the field
        can't be empty & has to be longer than 3 characters.
        """
        username = self.cleaned_data['username']

        if len(username) < 3:
            raise ValidationError(
                'Give yourself a username that is at least 3 characters.'
            )
        return username
