from django.db import models
from django.utils.translation import gettext_lazy as _
from core.common import BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator
from constants.constants import MIN_PRODUCT_WEIGHT, MAX_PRODUCT_WEIGHT, PRODUCT_NAME_MAX_LENGTH, PRODUCT_WEIGHT_MAX_DIGIT, PRODUCT_WEIGHT_DECIMAL_PLACES




class Product(BaseModel):
    name = models.CharField(max_length=PRODUCT_NAME_MAX_LENGTH, unique=True, db_index=True, verbose_name=_("Name"))
    # Validate the contact number to ensure it contains only numeric characters.
    weight = models.DecimalField(
        max_digits=PRODUCT_WEIGHT_MAX_DIGIT,
        decimal_places=PRODUCT_WEIGHT_DECIMAL_PLACES,
        validators=[
            MinValueValidator(MIN_PRODUCT_WEIGHT,message=_("Weight must be a positive decimal."),),
            MaxValueValidator(MAX_PRODUCT_WEIGHT, message=_("Weight must not be more than 25kg.")),
        ],
        help_text=_("Weight in kilograms."),
        verbose_name=_("Weight"),
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name
