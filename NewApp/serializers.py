from .models import Product, Category, Manufacturer, Cart, CartElement,Order,OrderElement
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = '__all__'

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Manufacturer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name=serializers.ReadOnlyField(source='category.name')
    manufacturer_name = serializers.ReadOnlyField(source='manufacturer.name')
    class Meta:
        model=Product
        fields = '__all__'

class CartElementSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    total_price = serializers.SerializerMethodField()
    class Meta:
        model=CartElement
        fields = ['id', 'cart', 'product', 'product_id', 'quantity', 'total_price']
        read_only_fields = ['cart']

    def get_total_price(self, obj):
        return obj.elem_price()

class CartSerializer(serializers.ModelSerializer):
    items = CartElementSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
   
    class Meta:
        model=Cart
        fields = ['id', 'user', 'creation_date', 'items', 'total_price']
        read_only_fields = ['user', 'creation_date']

    def get_total_price(self, obj):
        return obj.total_price()

