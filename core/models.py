# class BaseModel(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)

#     class Meta:
#         abstract = True

#     def soft_delete(self):
#         """Mark the object as deleted without removing it from the database."""
#         self.deleted_at = timezone.now()
#         self.is_active = False
#         self.save(update_fields=["deleted_at", "is_active"])

#     def restore(self):
#         """Undo a soft delete."""
#         self.deleted_at = None
#         self.is_active = True
#         self.save(update_fields=["deleted_at", "is_active"])


from django.db import models
import uuid
from django.utils import timezone


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
