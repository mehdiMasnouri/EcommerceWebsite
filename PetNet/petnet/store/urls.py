from django.urls import path
from .views import success, checkout, change_quantity, product_detail ,category_detail , search , add_to_cart , cart_view , remove_from_cart


urlpatterns=[
    path('search/', search, name='search'),
    path('add-to-cart/<int:product_id>/',add_to_cart,name='add-to-cart'),
    path('change-quantity/<str:product_id>/',change_quantity,name='change_quantity'),
    path('remove-from-cart/<str:product_id>/',remove_from_cart,name='remove_from_cart'),
    path('cart/',cart_view,name='cart_view'),
    path('cart/checkout/',checkout,name='checkout'),
    path('cart/success/',success,name='success'),
    path('<slug:category_slug>/<slug:slug>/',product_detail,name='product_detail'),
    path('<slug:slug>/',category_detail,name='category_detail'),


]