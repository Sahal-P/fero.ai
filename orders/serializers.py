from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from customers.models import Customer
from django.db import transaction
from django.db.models import Sum
from django.db import IntegrityError
from constants.constants import MAX_CUMULATIVE_WEIGHT


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()

    class Meta:
        model = OrderItem
        fields = ["id", "product_id", "quantity"]

    # def validate_product_id(self, value):
    #     if not Product.objects.filter(id=value).exists():
    #         raise serializers.ValidationError("Invalid product ID. Product does not exist.")
    #     return value


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    customer_id = serializers.UUIDField(required=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_id",
            "order_date",
            "address",
            "order_number",
            "order_items",
        ]

    def validate_customer_id(self, value):
        if not Customer.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                "Invalid customer ID. Customer does not exist."
            )
        return value

    def validate_order_items(self, order_items):
        product_ids = [order_item["product_id"] for order_item in order_items]
        try:
            products = Product.objects.filter(id__in=product_ids).values("weight", "id")

            product_weights = {product["id"]: product["weight"] for product in products}

            cumulative_weight = sum(
                product_weights[order["product_id"]] * order["quantity"]
                for order in order_items
            )
        except:
            raise serializers.ValidationError(
                "Invalid product ID. Product does not exist."
            )

        if cumulative_weight > MAX_CUMULATIVE_WEIGHT:
            raise serializers.ValidationError(
                f"Cumulative weight of order items cannot exceed {MAX_CUMULATIVE_WEIGHT}kg."
            )

        return order_items

    @transaction.atomic()
    def create(self, validated_data: dict):
        order_items_data = validated_data.get("order_items", [])
        order = Order.objects.select_related("order_items").create(
            address=validated_data["address"], customer_id=validated_data["customer_id"]
        )

        order_items = [
            OrderItem(order=order, **order_item_data)
            for order_item_data in order_items_data
        ]
        OrderItem.objects.bulk_create(order_items)
        return order

    @transaction.atomic()
    def update(self, instance, validated_data):
        order_items_data = validated_data.pop("order_items", [])

        instance.address = validated_data.get("address", instance.address)
        instance.save()

        updated_order_items = [
            OrderItem.objects.update_or_create(
                id=order_item_data.get("id"),
                order=instance,
                defaults={
                    "product_id": order_item_data.get("product_id"),
                    "quantity": order_item_data.get("quantity"),
                },
            )[0]  # inserting the first element of the tuple returned by update_or_create eg: updated , created =
            for order_item_data in order_items_data
        ]
        # OrderItem.objects.filter(order=instance).exclude(id__in=[item.id for item in updated_order_items]).delete()
        instance.order_items.exclude(
            id__in=[item.id for item in updated_order_items]
        ).delete()

        return instance


class GetOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        
class GetOrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'