from django.shortcuts import render
from store.models import Product
# Create your views here.


def frontpage(request):
    products = Product.objects.filter(status=Product.ACTIVE)[0:6]
    # products = Product.objects.all()[0:6]

    
    context = {'products' : products}
    return render(request,'core/frontpage.html',context=context)

def about(request):
    return render(request,'core/about.html')