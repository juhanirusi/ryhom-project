from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Our custom user model.
    """

    class Gender(models.TextChoices):
        Female = 'Female'
        Male = 'Male'
        Transgender = 'Transgender'
        Nonbinary = 'Non-binary/non-conforming'
        No_Response = 'Prefer not to respond'

    name = models.CharField(max_length=255)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    gender = models.CharField(
        max_length=12,
        choices=Gender.choices,
        default=Gender.No_Response)
    # birthday = models.DateField()
    bio = models.CharField(max_length=160, blank=True)
    # location = pip install django-location-field
    avatar = models.ImageField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    slug = models.SlugField(default='', blank=True, null=False, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'email', 'password', 'name']


    def get_absolute_url(self):
        return reverse('user-profile', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(UserProfile, self).save(*args, **kwargs)

    # def get_full_name(self):
    #     return self.name

    # def get_first_name(self):
    #     return self.name.split()[0]

    def __str__(self):
        return self.name
