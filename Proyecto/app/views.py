from django.shortcuts import render
from .models import*

# Create your views here.
def store(request):
    products = Product.objects.all()
    context = {'product':products}
    return render(request,'Generales/store.html')

def cart(request):
    context = {}
    return render(request,'Generales/cart.html')

def checkout(request):
    context = {}
    return render(request,'Generales/checkout.html')