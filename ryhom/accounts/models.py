from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
#from django.urls import reverse
from django.utils.text import slugify

from .managers import UserManager

# Create your models here.


class UserProfile(AbstractBaseUser, PermissionsMixin):
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
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    gender = models.CharField(
        max_length=25,
        choices=Gender.choices,
        default=Gender.NO_RESPONSE)
    # birthday = models.DateField()
    bio = models.CharField(max_length=160, blank=True)
    # location = pip install django-location-field
    avatar = models.ImageField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    slug = models.SlugField(default='', blank=True, null=False, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name'] # username/pass required by default!

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


    # def get_absolute_url(self):
    #     return reverse('user-profile', args=[self.slug])

    # EITHER ONE OF THESE!

    # def get_absolute_url(self):
    #     return reverse("accounts:detail", kwargs={"slug": self.slug})


    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(UserProfile, self).save(*args, **kwargs)


    def get_full_name(self):
        return self.name


    def get_short_name(self):
        return self.name.split()[0]


    def __str__(self):
        return self.name
