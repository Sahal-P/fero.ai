from django.db import models
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator
from core.common import BaseModel
from customers.models import Customer
from products.models import Product
from constants.constants import MAX_ORDER_NUMBER, MIN_ORDER_ITEM_QUANTITY, ORDER_ADDRESS_MAX_LENGTH

class Order(BaseModel):
    order_number = models.CharField(
        max_length=MAX_ORDER_NUMBER,
        unique=True,
        editable=False,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r"^ORD\d{5}$",
                message=_(
                    "Order number must match the pattern ORD followed by 5 digits."
                ),
            ),
        ],
        verbose_name=_("Order number"),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="order")
    order_date = models.DateField(verbose_name=_("Order date"), auto_now_add=True)
    address = models.CharField(max_length=ORDER_ADDRESS_MAX_LENGTH, verbose_name=_("Address"))

    def save(self, *args, **kwargs):
        
        with transaction.atomic():
            if not self.order_number:
                last_order_number = (
                    Order.objects.values_list("order_number", flat=True)
                    .order_by("-order_number")
                    .first()
                )
                last_order_number = int(last_order_number[3:]) if last_order_number else 0
                self.order_number = f"ORD{last_order_number + 1:05d}"

            super().save(*args, **kwargs)
            
    def __str__(self):
        return f"{self.order_number} - {self.customer.name}"

    class Meta:
        ordering = ["-order_date"]
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        
    # def save_with_retry(self, *args, **kwargs):
    #     max_retries = 3  # Adjust as needed
    #     retry_count = 0

    #     while retry_count < max_retries:
    #         try:
    #             self.save(*args, **kwargs)
    #             break  # Save successful, exit loop
    #         except IntegrityError:
    #             # Unique constraint violation, retry
    #             retry_count += 1
    #             # You may want to log the error or take other actions here

    #     if retry_count == max_retries:
    #         # Log or raise an exception since retries were unsuccessful
    #         raise IntegrityError("Unable to save with unique constraint after multiple attempts")

class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                limit_value=MIN_ORDER_ITEM_QUANTITY, message=f"Quantity must be minimum {MIN_ORDER_ITEM_QUANTITY}."
            )
        ]
    )

    def __str__(self):
        return (
            f"{self.quantity} x {self.product.name} (Order: {self.order.order_number})"
        )
