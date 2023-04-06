from django.shortcuts import render ,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Userprofile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect , render
from store.forms import ProductForm
from store.models import Product  ,Order ,OrderItem
from django.utils.text import slugify
from django.contrib import messages






def vendor_detail(request,pk):
    user = User.objects.get(pk=pk)
    products = user.products.filter(status=Product.ACTIVE)
    context= {'user':user,
              'products':products}
    return render(request,'userprofile/vendor_detail.html',context=context)

    
# decorator
@login_required
def my_store(request):
    products = request.user.products.exclude(status=Product.DELETED)
    order_items= OrderItem.objects.filter(product__user=request.user)
    context={'products':products,
             'order_items':order_items}
    return render(request,'userprofile/my_store.html',context)


@login_required
def my_store_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    return render(request, 'userprofile/my_store_order_detail.html', {
        'order': order
    })


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)

        if form.is_valid():
            title= request.POST.get('title')
            product = form.save(commit=False)
            product.user= request.user
            product.slug= slugify(title)
            product.save()

            messages.success(request,'The product was added')

            return redirect('my_store')
    else:
        form= ProductForm()
    # context = {'form':form}
    return render(request,'userprofile/product_form.html',{'title':'Edit Product','form':form})




@login_required
def edit_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            messages.success(request,'changes was saved!')
            return redirect('my_store')

    else:
        form= ProductForm(instance=product)
    # context = {'form':form}
    return render(request,'userprofile/product_form.html',
                  {'title':'Edit Product',
                   'form':form ,
                   'product':product
                   })





@login_required
def delete_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.status = Product.DELETED
    product.save()
    messages.success(request,'The product was deleted')

    return redirect('my_store')



@login_required
def  myaccount(request):
    return render(request,'userprofile/myaccount.html')


def signup(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)


        if form.is_valid():
            user = form.save()
            login(request,user)
            userprofile = Userprofile.objects.create(user=user)

            return redirect('frontpage')
    else:
        form= UserCreationForm()

    context = {'form':form}


    return render(request,'userprofile/signup.html', context=context)

    






        

 