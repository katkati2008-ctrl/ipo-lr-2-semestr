from .models import Product, Category, Manufacturer, Cart, CartElement,Order,OrderElement,Profile
from rest_framework import serializers
from django.contrib.auth.models import User


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
   
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'full_name', 'phone', 'address', 'role', 'role_display','city']
        read_only_fields = ['role']

class OrderElementSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    item_total = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderElement
        fields = ['id', 'order', 'product', 'product_name', 
                  'product_price', 'quantity', 'item_total']
    
    def get_item_total(self, obj):
        return obj.product.price * obj.quantity


class OrderSerializer(serializers.ModelSerializer):
    items = OrderElementSerializer(many=True, read_only=True)
    username = serializers.ReadOnlyField(source='user.username')
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'username', 'home_address', 
                  'num_phone', 'email', 'items', 'total_price', 'date_time']
        read_only_fields = ['user', 'date_time', 'total_price']


