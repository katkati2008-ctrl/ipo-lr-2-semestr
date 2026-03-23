from .models import Product, Category, Manufacturer, Cart, CartElement,Order,OrderElement
from django.conf import settings
from rest_framework import routers, serializers, viewsets

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = '__all__'

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Manufacturer
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields = '__all__'

class CartElementSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartElement
        fields = '__all__'

