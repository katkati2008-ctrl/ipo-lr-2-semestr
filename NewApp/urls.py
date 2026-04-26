from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'products',views.ProductViewSet,basename='products')
router.register(r'categories',views.CategoryViewSet,basename='categories')
router.register(r'manufacturers',views.ManufacturerViewSet,basename='manufactures')
router.register(r'carts',views.CartViewSet,basename='carts')
router.register(r'cart-elements',views.CartElementViewSet,basename='cart-items')

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
    path('checkout/',views.checkout,name="checkout"),
    path('register/',views.register,name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/', include(router.urls)),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
]   

