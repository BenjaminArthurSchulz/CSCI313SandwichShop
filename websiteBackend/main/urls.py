import django
from django.urls import include, path
from . import views

urlpatterns = [
    path("logout/", views.LogOut, name="logout"),
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("sign-up", views.sign_up, name="sign-up"),
    path("", include("django.contrib.auth.urls")),  
]

# Checkout URLs
urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
]