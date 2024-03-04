from django.shortcuts import render

# Create your views here.
def store(request):
    context = {}
    return render(request,'Generales/store.html')

def cart(request):
    context = {}
    return render(request,'Generales/cart.html')

def checkout(request):
    context = {}
    return render(request,'Generales/checkout.html')