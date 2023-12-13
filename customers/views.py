from rest_framework.request import Request
from rest_framework.views import APIView
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.response import Response
from rest_framework import status, exceptions, serializers
from django.shortcuts import get_object_or_404
from helpers.helpers import get_id
from core.exceptions import InternalError

"""
    Customers:
    o List all customers: GET /api/customers/
    o Create a new customer: POST /api/customers/
    o Update exiting customer: PUT /api/customers/<id>/
"""

class CustomerAPIView(APIView):
    serializer_class = CustomerSerializer
    
    def get(self, request: Request) -> Response:
        try:
            queryset = Customer.objects.all()
            serializer = CustomerSerializer(queryset, many=True)
        except Exception as e:
            raise InternalError(e)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            serializer = CustomerSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except serializers.ValidationError as error:
            raise error
        except Exception as e:
            raise InternalError(e)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request: Request) -> Response:
        try:
            customer_id = get_id(request)
            customer = get_object_or_404(Customer, pk=customer_id)
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except serializers.ValidationError as error:
            raise error
        except Exception as e:
            raise InternalError(e)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request) -> Response:
        try:
            customer_id = get_id(request)
            customer = get_object_or_404(Customer, pk=customer_id)
            serializer = CustomerSerializer(customer, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except serializers.ValidationError as error:
            raise error
        except Exception as e:
            raise InternalError(e)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request) -> Response:
        try:
            customer_id = get_id(request)
            customer = get_object_or_404(Customer, pk=customer_id)
            customer.delete()
        except Exception as e:
            raise InternalError(e)
        return Response(status=status.HTTP_204_NO_CONTENT)

