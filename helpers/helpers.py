from django.http import HttpRequest
from rest_framework import serializers
from rest_framework.request import Request

def get_id(request: Request) -> str:
    
    # If sending 'id' as a query param 
    _id = request.query_params.get('id', None)
    if _id is None:
        _id = request.data.get("id", None)
    if _id is None:
        raise serializers.ValidationError({"id": ["This field is required."]})
    return _id
