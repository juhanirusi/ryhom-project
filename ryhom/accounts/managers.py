from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, name, username, email,
                    password=None, **extra_fields):
        """Create, save and return a new user."""

        if not name:
            raise ValueError('All users must have a name!')
        if not username:
            raise ValueError('All users must have a username!')
        if not email:
            raise ValueError('All users must have an email address!')

        email = self.normalize_email(email)

        user = self.model(
            name=name,
            username=username,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, email, password, name, username):
        """Create and return a new superuser."""
        user = self.create_user(
            name=name,
            username=username,
            email=email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
