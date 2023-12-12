from django.db import models
import uuid
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

MAX_CONTACT_NUMBER_LENGTH = 15


class BaseModel(models.Model):
    # Used UUID as the primary key for better consistency and security.
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )

    class Meta:
        abstract = True


class Customer(BaseModel):
    
    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name=_("Name"))
    # Validate the contact number to ensure it contains only numeric characters.
    contact_number = models.CharField(
        max_length=MAX_CONTACT_NUMBER_LENGTH,
        validators=[
            RegexValidator(
                regex=r"^\d{1,"+ str(MAX_CONTACT_NUMBER_LENGTH) + r"}$",
                message="Contact number must contain only numeric characters.",
            )
        ],
        verbose_name=_("Contact Number"),
    )
    email = models.EmailField(unique=True, db_index=True, verbose_name=_("Email"))

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("Customers")

    def __str__(self):
        return self.name
