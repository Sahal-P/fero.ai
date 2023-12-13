from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from constants.constants import MAX_CONTACT_NUMBER_LENGTH, CUSTOMER_NAME_MAX_LENGTH
from core.common import BaseModel


class Customer(BaseModel):
    
    name = models.CharField(max_length=CUSTOMER_NAME_MAX_LENGTH, unique=True, db_index=True, verbose_name=_("Name"))
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
