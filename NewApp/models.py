from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    price=models.DecimalField(max_digits=10,verbose_name='Цена', decimal_places=2,validators=[MinValueValidator(0)])
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
    
    def valid_elem(self):
        if self.quantity > self.product.quantity:
            raise ValidationError("Нет в наличии")
    
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user',verbose_name='Пользователь')
    home_address=models.CharField(max_length=300,verbose_name='Ваш адрес')
    num_phone=models.CharField(max_length=25,verbose_name='Номер телефона')
    email = models.EmailField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Стоимость заказа")
    date_time=models.DateTimeField(auto_now_add=True,verbose_name="Время и дата заказа")

    def __str__(self):
        return f"Заказ №{self.id},пользователя {self.user.username}"
    
class OrderElement(models.Model):
       order=models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name='Заказ')
       product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='Товар')
       quantity=models.PositiveIntegerField(verbose_name='Количество')
       price=models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])

class Profile(models.Model):
    class Role(models.TextChoices):
         CUSTOMER = 'customer', 'Покупатель'
         MANAGER = 'manager', 'Менеджер'
         ADMIN = 'admin', 'Администратор'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True)
    address = models.TextField(verbose_name='Адрес доставки', blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER, verbose_name='Роль')
    city = models.CharField(max_length=100, verbose_name='Город', blank=True)

    def __str__(self):
        return f"Профиль {self.user.username}"
    
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.user.is_superuser
    
    def is_manager(self):
        return self.role == self.Role.MANAGER or self.user.is_staff
 
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            full_name=f"{instance.first_name} {instance.last_name}".strip() or instance.username
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()    



    





# Create your models here.
