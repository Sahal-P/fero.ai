from rest_framework.views import APIView
from rest_framework.request import Request
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status, exceptions, serializers
from django.shortcuts import get_object_or_404
from helpers.helpers import get_id
from core.exceptions import InternalError
"""
    Products:
    o List all Products: GET /api/Products/
    o Create a new Product: POST /api/Products/
    o Update exiting Product: PUT /api/Products/<id>/
"""

class ProductAPIView(APIView):
    serializer_class = ProductSerializer
    
    def get(self, request: Request) -> Response:
        try:
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset, many=True)
        except Exception as e:
            raise InternalError(e)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            serializer = ProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except serializers.ValidationError as error:
            raise error
        except Exception as e:
            raise InternalError(e)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request: Request) -> Response:
        try:
            product_id = get_id(request)
            product = get_object_or_404(Product, pk=product_id)
            serializer = ProductSerializer(product, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except serializers.ValidationError as error:
            raise error
        except Exception as e:
            raise InternalError(e)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request) -> Response:
        try:
            product_id = get_id(request)
            product = get_object_or_404(Product, pk=product_id)
            serializer = ProductSerializer(product, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except serializers.ValidationError as error:
            raise error
        except Exception as e:
            raise InternalError(e)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request) -> Response:
        try:
            product_id = get_id(request)
            product = get_object_or_404(Product, pk=product_id)
            product.delete()
        except Exception as e:
            raise InternalError(e)
        return Response(status=status.HTTP_204_NO_CONTENT)

