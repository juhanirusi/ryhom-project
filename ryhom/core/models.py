import uuid

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
        db_index=True
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
