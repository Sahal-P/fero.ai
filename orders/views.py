from rest_framework.views import APIView
from rest_framework.request import Request
from .models import Product
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework import status, exceptions, serializers
from django.shortcuts import get_object_or_404
from helpers.helpers import get_id
from core.exceptions import InternalError

# from django.db import connection

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

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            order_serializer = OrderSerializer(data=request.data)
            if order_serializer.is_valid(raise_exception=True):
                order_serializer.save()
        except Exception as e:
            raise InternalError(e)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)