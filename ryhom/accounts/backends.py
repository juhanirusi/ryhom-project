from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db.models import Q

User = get_user_model()


# Our custom backend class that allows the user login into their
# account either with their email or unique username
class EmailUsernameAuthBackend(object):
    def authenticate(self, request, username=None, email=None, password=None):
        try:
            user = User.objects.get(
                Q(email=email) | Q(username=username)
            )

        except User.DoesNotExist:
            return None

        if user and check_password(password, user.password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
