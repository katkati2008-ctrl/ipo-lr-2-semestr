from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Category(models.Model):
    name=models.CharField(max_length=100,verbose_name='Категория товара')
    description=models.TextField(blank=True,verbose_name='Описание категории')
    
    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name=models.CharField(max_length=100,verbose_name='Производитель')
    country=models.CharField(max_length=100,verbose_name='Страна производителя')
    description=models.TextField(blank=True,verbose_name='Описание производителя')

    def __str__(self):
        return self.name


class Product(models.Model):
    name=models.CharField(max_length=200,verbose_name='Название товара')
    description=models.TextField(null=False,verbose_name='Описание товара')
    product_image=models.ImageField(upload_to='product/')
    price=models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    quantity=models.IntegerField(validators=[MinValueValidator(0)])
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    manufacturer=models.ForeignKey(Manufacturer,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='Пользователь')
    creation_date=models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"
    
    def total_price(self):
        total_pr=0
        for item in self.items.all():
            total_pr +=item.product.price * item.quantity
        return total_pr

    

class CartElement(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items',verbose_name='Корзина')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='Товар')
    quantity=models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return f"{self.product} ({self.quantity} шт.)"
    
    def elem_price(self):
        return self.product.price * self.quantity
    
    def valid_price(self):
        if self.quantity > self.product.quantity:
            raise ValidationError("Нет в наличии")
    
class Order(models.model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user',verbose_name='Пользователь')
    home_address=models.CharField(max_length=300,related_name='home_address',verbose_name='Ваш адрес')
    num_phone=models.CharField(max_length=25,related_name='num_phone',verbose_name='Номер телефона')
    total_price = models.DecimalField(max_digits=10,decimal_places=2,related_name='total_price',verbose_name="Стоимость заказа")


    





# Create your models here.
