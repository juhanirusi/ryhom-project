from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile


class RegisterUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['username'].widget.attrs['placeholder'] = 'Käyttäjätunnus'
        # self.fields['username'].label = ''

        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    class Meta:
        model = UserProfile
        fields = ('email', 'username', 'name', 'password1', 'password2')

        labels = {
            'username'  : 'Pick a Username',
            'name'      : 'Full Name',
            'password1' : 'Pick a Password',
            'password2' : 'Enter Your Password Again',
        }
