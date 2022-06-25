from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Generate a token that will be added to the confirmation email
    that's sended to the user after successful registration.
    """
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )

account_token_generator = AccountActivationTokenGenerator()
