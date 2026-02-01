from rest_framework import serializers
from .models import Book

class bookSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields='__all__'

def validate_price(self,value):
    if value<0:
        raise serializers.ValidationError('price must be > 0')
    return value