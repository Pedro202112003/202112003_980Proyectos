from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.store, name='Tienda'),
    path('cart/',views.cart, name='carrito'),
    path('checkout/', views.checkout, name='pago'),
]
