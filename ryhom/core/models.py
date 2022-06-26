# from django.db import models
# import uuid

# LET'S ADD A BASE MODEL HERE THAT WE'RE GOING TO USE ACROSSS
# OUR OTHER MODELS. FOR EXAMPLE, CODE LIKE THIS...

# class BaseAbstractModel(models.Model):

#     """
#      This model defines base models that implements common fields like:
#      created_at
#      updated_at
#      is_deleted
#     """
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, null=False, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True, editable=False)
#     updated_at = models.DateTimeField(auto_now=True, editable=False)
#     is_deleted = models.BooleanField(default=False)

#     def soft_delete(self):
#         """soft  delete a model instance"""
#         self.is_deleted=True
#         self.save()

#     class Meta:
#         abstract = True
#         ordering = ['-created_at']
