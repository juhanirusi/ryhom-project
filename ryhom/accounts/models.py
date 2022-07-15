import itertools
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ryhom.core.utils import resize_optimize_image

from .managers import AccountManager

allowed_file_extensions = ['jpg', 'png', 'jpeg']

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
        FEMALE = 'Female', 'Female'
        MALE = 'Male', 'Male'
        TRANSGENDER = 'Transgender', 'Transgender'
        NONBINARY = 'Non-binary', 'Non-binary/non-conforming'
        NO_RESPONSE = 'No response', 'Prefer not to respond'

    # Our additional UUID field for public lookups.
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
        max_length=25,
        choices=Gender.choices,
        default=Gender.NO_RESPONSE)
    birthday = models.DateField(null=True, blank=True)
    bio = models.CharField(max_length=160, blank=True, default='')
    profile_image = models.ImageField(blank=True,
        upload_to='accounts/profile-images/',
        validators=[FileExtensionValidator(allowed_file_extensions)]
    )
    website = models.URLField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    slug = models.SlugField(default='', blank=True, null=False, unique=True)

    objects = AccountManager()

    # Let's change the email field to be the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        #indexes = [models.Index(fields=['uuid', 'slug'])]
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

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
        name = ''.join(self.name.split())
        slug = unique_slug = slugify(name) # Same value to 2 variables

        for num in itertools.count(1):
            if not Account.objects.filter(slug=unique_slug).exists():
                break
            unique_slug = '{}{}'.format(slug, num)

        self.slug = unique_slug


    def save(self, *args, **kwargs):
        """Override save method to generate a URL slug & username"""

        if not self.slug:
            self._create_slug()
            if not self.username:
                self.username = self.slug

        # A BUZZFEED.COM LIKE RANDOM PROFILE IMAGE...

        # IMAGES = [ <-- ADD TO THE TOP OF THE MODEL!
        #     'profile1.jpg', 'profile2.jpg', 'profile3.jpg', 'profile4.jpg', 'profile5.jpg',
        #     'profile6.jpg', 'profile7.jpg', 'profile8.jpg', 'profile9.jpg', 'profile10.jpg',
        # ]
        # if self.image == 'default.jpg': <-- MAKE A LIST OF IMAGES
        #     self.image = random.choice(self.IMAGES)

        # RESIZE THE IMAGE TO A SPECIFIC SIZE...

        # super(Account, self).save(*args, **kwargs) <-- NOT SURE IF SHOULD CALL THIS BEFORE THE IMAGE CODE?!
        # img = Image.open(self.image.path)

        # if img.height > 300 or img.width > 300:
        #     output_size = (300, 300)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)
        if self.profile_image != self.__original_profile_image:
            if self.profile_image != '':
                self.profile_image = resize_optimize_image(
                                        self.profile_image,
                                        desired_width=500,
                                        desired_height=500
                                    )
        self.__original_profile_image = self.profile_image
        super(Account, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse(
            'accounts:user_profile', kwargs={'user_profile_slug': self.slug}
        )


    def get_full_name(self):
        """Get user's full name."""
        return self.name


    def get_short_name(self):
        """Only get user's first name'"""
        return self.name.split()[0]


    def __str__(self):
        """How an instance of Account is shown in admin"""
        return self.name
