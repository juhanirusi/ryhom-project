from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
#from django.urls import reverse
from django.utils.text import slugify

from .managers import AccountManager

# Create your models here.


class Account(AbstractBaseUser, PermissionsMixin):
    """
    Our custom user model that contains additional fields
    and a function to slugify the user's username.
    """

    class Gender(models.TextChoices):
        FEMALE = 'Female', 'Female'
        MALE = 'Male', 'Male'
        TRANSGENDER = 'Transgender', 'Transgender'
        NONBINARY = 'Non-binary', 'Non-binary/non-conforming'
        NO_RESPONSE = 'No response', 'Prefer not to respond'

    name = models.CharField(max_length=255)
    username = models.CharField(max_length=50, unique=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    gender = models.CharField(
        max_length=25,
        choices=Gender.choices,
        default=Gender.NO_RESPONSE)
    birthday = models.DateField(null=True, blank=True)
    bio = models.CharField(max_length=160, blank=True)
    profile_image = models.ImageField(blank=True, upload_to='profile-images/')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    slug = models.SlugField(default='', blank=True, null=False, unique=True)

    objects = AccountManager()

    # Let's change the email field to be the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


    # def get_absolute_url(self):
    #     return reverse('user-profile', args=[self.slug])

    # EITHER OF THESE!

    # def get_absolute_url(self):
    #     return reverse("accounts:detail", kwargs={"slug": self.slug})


    def _create_slug(self):
        """
        Remove all whitespace from the name. Then check if slug
        already exists in the database. If it does exists, add
        a number after the slug until the database doesn't
        contain any other matching slug.
        """
        name = ''.join(self.name.split())
        slug = slugify(name)
        unique_slug = slug
        num = 1

        while Account.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}{}'.format(slug, num)
            num += 1

        return unique_slug


    def save(self, *args, **kwargs):
        """Override save method to generate a URL slug & username"""
        if not self.slug:
            self.slug = self._create_slug()
            if not self.username:
                self.username = self.slug
        super(Account, self).save(*args, **kwargs)


    def get_full_name(self):
        """Get user's full name."""
        return self.name


    def get_short_name(self):
        """Only get user's first name'"""
        return self.name.split()[0]


    def __str__(self):
        return self.name
