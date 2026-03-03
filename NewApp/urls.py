from django.urls import path
from . import views
from product import *



urlpatterns = [
    path('',views.main,name='main'),
    path('about/',views.about,name='about'),
    path('author/',views.author,name='author'),
    path('catalog/',views.product_list,name='product_list'),
    path('catalog/<int:pk>/',views.product_detail,name='product_detail'),
    path('cart/add/<int:item_id>/',views.add_to_cart,name='add_to_cart'),
    path('cart/update/<int:item_id>/',views.update_cart,name='update_cart'),
    path('cart/remove/<int:item_id>/',views.remove_from_cart,name='remove_from_cart'),
    path('cart/',views.cart_view,name='cart_view'),
]

