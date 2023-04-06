from django.urls import path
from .views import my_store_order_detail , vendor_detail ,signup , myaccount ,my_store ,add_product ,edit_product , delete_product
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/',signup,name='signup'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('login/',auth_views.LoginView.as_view(template_name='userprofile/login.html'),name='login'),
    path('myaccount/',myaccount,name='myaccount'),
    path('my-store/',my_store,name='my_store'),
    path('my-store/order-detail/<int:pk>/',my_store_order_detail,name='my_store_detail'),
    path('my-store/add-product/',add_product,name='add_product'),
    path('my-store/edit-product/<int:pk>/',edit_product,name='edit_product'),
    path('my-store/delete-product/<int:pk>/',delete_product,name='delete_product'),

    path('vendors/<int:pk>/',vendor_detail,name='vendor_detail'),

]