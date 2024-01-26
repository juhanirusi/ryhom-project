import itertools
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from ryhom.core.utils import resize_optimize_image

from .managers import AccountManager

# What image extensions the profile image field allows
ALLOWED_FILE_EXTENSIONS = ["jpg", "png", "jpeg"]
DEFAULT_PROFILE_IMAGE = "default-profile-image.jpg"


class Account(AbstractBaseUser, PermissionsMixin):
    """
    Our custom user model that contains additional fields
    and a function to slugify the user's username.

    Our model also contains an UUID field. We'll keep Django's own
    sequential id as primary key, but add an additional UUID field
    to the model because it's going to be a safer method for public
    model lookups like APIs.
    """

    class Gender(models.TextChoices):
        FEMALE = "Female", "Female"
        MALE = "Male", "Male"
        TRANSGENDER = "Transgender", "Transgender"
        NONBINARY = "Non-binary", "Non-binary/non-conforming"
        NO_RESPONSE = "No response", "Prefer not to respond"

    # Our additional UUID field for public lookups. For example, API access
    # We're still using a normal auto incrementing primary key
    # for querying inside our program!
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        null=False,
        unique=True,
    )
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    gender = models.CharField(
        max_length=25, choices=Gender.choices, default=Gender.NO_RESPONSE
    )
    birthday = models.DateField(null=True, blank=True)
    bio = models.CharField(max_length=160, blank=True, default="")
    profile_image = models.ImageField(
        blank=True,
        default=DEFAULT_PROFILE_IMAGE,
        upload_to="accounts/profile-images/",
        validators=[FileExtensionValidator(ALLOWED_FILE_EXTENSIONS)],
    )
    website = models.URLField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    slug = models.SlugField(default="", blank=True, null=False, unique=True)

    objects = AccountManager()

    # Let's change the email field to be the username field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]  # The name field is required

    class Meta:
        db_table = "account"  # Good to define table name!
        # indexes = [models.Index(fields=['uuid', 'slug'])]
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    __original_profile_image = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_profile_image = self.profile_image

    def _create_slug(self):
        """
        Remove all whitespace from the name. Then check if slug
        already exists in the database. If it does exists, add
        a number after the slug until the database doesn't
        contain any other matching slug.
        """
        name = "".join(self.name.split())
        slug = unique_slug = slugify(name)  # Same value to 2 variables

        for num in itertools.count(1):
            if not Account.objects.filter(slug=unique_slug).exists():
                break
            unique_slug = "{}{}".format(slug, num)

        self.slug = unique_slug

    def _profile_image(self):
        """
        Check if the user has uploaded a profile image of themselves,
        if not, use the default profile image.
        """
        if self.profile_image:
            return self.profile_image
        return DEFAULT_PROFILE_IMAGE

    def save(self, *args, **kwargs):
        """Override save method to generate a URL slug & username"""

        if not self.slug:
            self._create_slug()
            if not self.username:
                self.username = self.slug

        self.profile_image = self._profile_image()
        if self.profile_image != DEFAULT_PROFILE_IMAGE:
            if self.profile_image != self.__original_profile_image:
                self.profile_image = resize_optimize_image(
                    self.profile_image, desired_width=500, desired_height=500
                )
            self.__original_profile_image = self.profile_image

        super(Account, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("accounts:user_profile", kwargs={"user_profile_slug": self.slug})

    def get_full_name(self):
        """Get user's full name."""
        return self.name

    def get_short_name(self):
        """Only get user's first name'"""
        return self.name.split()[0]

    def __str__(self):
        """How an instance of Account is shown in admin"""
        return self.name
