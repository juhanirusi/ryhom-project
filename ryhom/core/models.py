import uuid

from django.conf import settings
from django.db import models


class BaseAbstractModel(models.Model):
    """
    Our base model that we can subclass from when creating models.
    This model contains common fields that
    we tend to use on most of our models.

    Our model also contains an UUID field. We'll keep Django's own
    sequential id as primary key, but add an additional UUID field
    to the model because it's going to be a safer method for public
    model lookups like APIs.
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        null=False,
        unique=True,
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        #indexes = [models.Index(fields=['uuid'])]
        abstract = True


class BaseCommentModel(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        null=False,
        unique=True,
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True
    )
    comment = models.TextField() # <-- ADD A VALIDATOR TO FORM (50 to 6,000 CHARACTERS!)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
        related_name="replies", null=True, blank=True
    )

    class Meta:
        #indexes = [models.Index(fields=['uuid'])]
        abstract = True
