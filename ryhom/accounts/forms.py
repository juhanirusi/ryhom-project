from django.contrib.auth.forms import UserCreationForm

from .models import Account


class RegisterUserForm(UserCreationForm):
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
