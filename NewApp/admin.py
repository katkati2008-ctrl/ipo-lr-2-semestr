from django.contrib import admin
from .models import Manufacturer,Category,Product,Cart,CartElement,Order,OrderElement,Profile
from django.contrib.auth.models import User


admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartElement)
admin.site.register(Order)
admin.site.register(OrderElement)
admin.site.register(Profile)



# Register your models here.
