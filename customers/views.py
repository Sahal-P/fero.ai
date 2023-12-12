from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

"""
    Customers:
    o List all customers: GET /api/customers/
    o Create a new customer: POST /api/customers/
    o Update exiting customer: PUT /api/customers/<id>/
"""

class CustomerViewSet(GenericAPIView):
    serializer_class = CustomerSerializer
    
    def get(self, request):
        queryset = Customer.objects.all()
        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk=None):
        customer_id = request.data.get('id')
        customer = get_object_or_404(Customer, pk=customer_id)
        serializer = CustomerSerializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        customer_id = request.data.get('id')
        customer = get_object_or_404(Customer, pk=customer_id)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        customer_id = request.data.get('id')
        customer = get_object_or_404(Customer, pk=customer_id)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

