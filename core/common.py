from django.db import models
import uuid


class BaseModel(models.Model):
    # Used UUID as the primary key for better consistency and security.
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )

    class Meta:
        abstract = True