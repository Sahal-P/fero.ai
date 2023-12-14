from rest_framework.views import APIView
from rest_framework.request import Request
from .models import Product
from .serializers import OrderSerializer, GetOrderSerializer
from rest_framework.response import Response
from rest_framework import status, exceptions, serializers
from django.shortcuts import get_object_or_404
from helpers.helpers import get_id
from core.exceptions import InternalError
from django.db import IntegrityError
from orders.models import Order
from customers.models import Customer
from helpers.helpers import get_id
from django.db import connection

"""
    Orders:
        o List all orders: GET /api/orders/
        o Create a new order with multiple product and corresponding quantity: POST 
        /api/orders/
        o Edit existing order: PUT /api/orders/<id>/
        o List order based on the products: GET /api/orders/?products=Book,Pen
        o List order based on the customer: GET /api/orders/?customer=Sam
        
"""


class OrderAPIView(APIView):
    serializer_class = OrderSerializer

    def get_param(self, request: Request, param) -> str | None:
        return request.query_params.get(param, None)

    def get(self, request: Request, *args, **kwargs) -> Response:
        try:
            filter_by_products, filter_by_customer = self.get_param(
                request, "products"
            ), self.get_param(request, "customer")
            if filter_by_customer:
                orders = Order.objects.prefetch_related("order_items").filter(
                    customer__name=filter_by_customer
                )
            elif filter_by_products:
                products_name = filter_by_products.split(",")
                orders = (
                    Order.objects.prefetch_related("order_items__product")
                    .filter(
                        order_items__product__name__in=products_name
                    )
                    .distinct()
                )
                print(orders)
            else:
                orders = Order.objects.prefetch_related("order_items").all()
            order_serializer = GetOrderSerializer(instance=orders, many=True)
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        except Order.DoesNotExist:
            return Response(
                {"error": "No orders found."}, status=status.HTTP_404_NOT_FOUND
            )
        except serializers.ValidationError as validation_error:
            return Response(
                {"error": "Validation error.", "details": str(validation_error)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as internal_error:
            raise InternalError(internal_error)

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            order_serializer = OrderSerializer(data=request.data)
            if order_serializer.is_valid(raise_exception=True):
                order_serializer.save()
                return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as validation_error:
            raise validation_error
        except Exception as internal_error:
            raise InternalError(internal_error)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request: Request, *args, **kwargs) -> Response:
        try:
            order = Order.objects.get(id=get_id(request))
            order_serializer = OrderSerializer(instance=order, data=request.data)

            if order_serializer.is_valid(raise_exception=True):
                order_serializer.save()
                return Response(order_serializer.data, status=status.HTTP_200_OK)
            print(connection.queries)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except serializers.ValidationError as validation_error:
            raise validation_error
        except Exception as internal_error:
            raise InternalError(internal_error)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
