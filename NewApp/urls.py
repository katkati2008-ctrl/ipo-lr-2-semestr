from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import ProfileViewSet 

router = DefaultRouter()
router.register(r'products',views.ProductViewSet,basename='products')
router.register(r'categories',views.CategoryViewSet,basename='categories')
router.register(r'manufacturers',views.ManufacturerViewSet,basename='manufactures')
router.register(r'carts',views.CartViewSet,basename='carts')
router.register(r'cart-elements',views.CartElementViewSet,basename='cart-items')
router.register(r'profile', views.ProfileViewSet,basename='profile')
router.register(r'orders', views.OrderViewSet,basename='orders')


urlpatterns = [
    path('',views.main,name='main'),
    path('about/',views.about,name='about'),
    path('catalog/',views.product_list,name='product_list'),
    path('catalog/<int:pk>/',views.product_detail,name='product_detail'),
    path('cart/add/<int:item_id>/',views.add_to_cart,name='add_to_cart'),
    path('cart/update/<int:item_id>/',views.update_cart,name='update_cart'),
    path('cart/remove/<int:item_id>/',views.remove_from_cart,name='remove_from_cart'),
    path('cart/',views.cart_view,name='cart_view'),
    path('checkout/',views.checkout,name="checkout"),
    path('register/',views.register,name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main'), name='logout'),
    path('api/', include(router.urls)),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls')),
    path('profile/', views.profile_view, name='profile'),
]   

