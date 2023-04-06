from django.shortcuts import render , get_object_or_404 , redirect
from .models import Product , Category ,Order , OrderItem
from django.db.models import Q
from .cart import Cart
from django.contrib.auth.decorators import login_required
from . forms import OrderForm
from django.conf import settings
import json
import stripe
from django.http import JsonResponse



def add_to_cart(request,product_id):
    cart=Cart(request)
    cart.add(product_id)

    return redirect('frontpage')


def success(request):
    return render(request,'store/success.html')


def change_quantity(request, product_id):
    action = request.GET.get('action','')

    if action:
        quantity = 1
        if action=='decrease':
            quantity = -1
    
        cart= Cart(request)    
        cart.add(product_id,quantity,True)
    return redirect('cart_view')

def remove_from_cart(request,product_id):
    cart=Cart(request)
    cart.remove(product_id)
    return redirect('cart_view')


def cart_view(request):
    cart = Cart(request)
    context = {
        'cart':cart
    }
    return render(request, 'store/cart_view.html',context)


@login_required
def checkout(request):
    cart = Cart(request)

    if cart.get_total_cost()==0:
        return redirect('cart_view')

    if request.method == 'POST':
        data = json.loads(request.body)
        first_name = data['first_name']
        last_name = data['last_name']
        address = data['address']
        zipcode = data['zipcode']
        city = data['city']
        # if statement for checking form validation
        if first_name and last_name and address and zipcode and city:
            
            form = OrderForm(request.POST)
            total_price = 0
            items = []

            for item in cart:
                product = item['product']
                total_price += product.price * int(item['quantity'])

                items.append({
                    'price_data':{
                    'currency':'eur',
                    'product_data':{
                        'name': product.title,
                    },
                    'unit_amount': product.price
                    },
                    'quantity': item['quantity']
                })


            stripe.api_key = settings.STRIPE_SECRET_KEY
            #now creating session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=items,
                mode='payment',
                success_url= f'{settings.WEBSITE_URL}cart/success/',
                cancel_url = f'{settings.WEBSITE_URL}cart/',

            )
            payment_intent = session.payment_intent
            # print('\n\n\n---------------------------------------------')

            # print('type :' , type(payment_intent))
            # print('payment_intent' , payment_intent)

            # print('\n---------------------------------------------\n\n\n')
            #creating one order
            order = Order.objects.create(
                first_name=first_name,
                last_name=last_name,
                address=address,
                zipcode=zipcode,
                city=city,
                created_by = request.user,
                is_paid = True,
                # payment_intent = payment_intent,
                payment_intent = "1",
                paid_amount = total_price
            )

            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity
                #Creating several OrderItem
                item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

            cart.clear()

            # return redirect('myaccount')
            return JsonResponse({'session':session,'order':payment_intent})
        
    else:
        form = OrderForm()

    return render(request, 'store/checkout.html', {
        'cart': cart,
        'form': form,
        'pub_key':settings.STRIPE_PUB_KEY,
    })



def search(request):
    query = request.GET.get('query','')
    products = Product.objects.filter(status=Product.ACTIVE).filter(Q(title__icontains=query) | Q(description__icontains=query))
    context= {'query':query , 
              'products' :products}
    return render(request,'store/search.html',context=context)

def category_detail(request,slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(status=Product.ACTIVE)
    context = {'category':category ,
               'products': products ,
               }
    return render(request,'store/category_detail.html',context=context)

def product_detail(request,category_slug,slug):
    # product = Product.objects.get(slug=slug)
    product =  get_object_or_404(Product,slug=slug , status = Product.ACTIVE)
    context = {'product':product}
    return render(request,'store/product_detail.html',context=context)