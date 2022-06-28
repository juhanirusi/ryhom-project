from django.db import models
from ryhom.core.models import BaseAbstractModel


class Article(BaseAbstractModel):
    """Model for articles"""

    class Status(models.TextChoices):
        FEATURED = 'Featured', 'Featured'

    class Type(models.TextChoices):
        DEFAULT = 'Default', 'Default'
        MICRO = 'Micropost', 'Micropost (Under 300 Words)'

    title = models.CharField(max_length=150)
    #summary
    #author
    #image
    #content <-- CKEditor RichTextField(), RichTextUploadingField, or a simple models.TextField
    #image_credit <-- SHOW THE OWNER OF THE IMAGE
    #category <-- ManyToManyField
    #tags <-- ManyToManyField
    #slug
    #status <-- CHOICES.STATUS
    #featured <-- A SIMPLE BOOLEAN
    #likes <-- PositiveIntegerField
    #published <-- A SIMPLE BOOLEAN

    # class Meta:
    #     ordering = ['-created']
    #     unique_together = ('author', 'title') <-- One author can't have multiple posts with same title
    #     objects = models.Manager() <--- ASSIGN THE DEFAULT MODEL MANAGER BEFORE OUR CUSTOM ONES!

    # def total_likes(self):
    #     return self.likes.count()

    # def __str__(self):
    #     return self.title


#class Comment(models.Model):
    #post <-- Foreign Key (or OneToOneField?)
    #author <-- Foreign Key (or OneToOneField?)
    #title
    #comment
    #likes
    #approved = models.BooleanField(default=True) --> THINK ABOUT THIS IF IT'S EVEN NECESSARY WHEN
                                                    # THE USER NEEDS TO BE LOGGED IN IN THE FIRST PLACE!
    #date <-- SOME DATE WHEN COMMENT WAS WRITTEN
    #replies <-- SOMEHOW... LIKE THIS FOR EXAMPLE:

    # reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')

    # class Meta:
    #     ordering=["-date"]

    # @property
    # def children(self):
    #     return Comment.objects.filter(parent=self).order_by('-created_on').all()

    # @property
    # def is_parent(self):
    #     if self.parent is None:
    #         return True
    #     return False
