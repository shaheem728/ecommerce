from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:id>', views.Product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('contact/', views.contact_view, name='contact_view'),
    path('about/', views.about_view, name='about_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),  
    path('cart/quantity/<int:product_id>/<str:action>/', views.quantity, name='quantity'),

]

