from django.contrib import admin
from .models import Manufacturer,Category,Product,Cart,CartElement
from django.contrib.auth.models import User


admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartElement)


# Register your models here.
