from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from customers.models import Customer
from django.db import transaction
        
class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()
    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity']
    
    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product ID. Product does not exist.")
        return value

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    customer_id = serializers.UUIDField(required=True)
    class Meta:
        model = Order
        fields = ['customer_id', 'order_date', 'address', 'order_number', 'order_items']
    
    def validate_customer_id(self, value):
        if not Customer.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid customer ID. Customer does not exist.")
        return value
    
    @transaction.atomic()
    def create(self, validated_data: dict):
        order_items_data = validated_data.get('order_items',[])
        order = Order.objects.select_related('order_items').create(address=validated_data['address'], customer_id=validated_data["customer_id"])

        order_items = [
            OrderItem(order=order, **order_item_data)
            for order_item_data in order_items_data
        ]
        OrderItem.objects.bulk_create(order_items)
        return order