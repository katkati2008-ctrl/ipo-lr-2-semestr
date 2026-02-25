from django.urls import path
from . import views
from product import *

urlpatterns = [
    path('',views.main,name='main'),
    path('about/',views.about,name='about'),
    path('author/',views.author,name='author')
]