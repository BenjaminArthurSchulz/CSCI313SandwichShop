import django
from django.urls import path, include
from . import views
from .views import clear_cart

# Registratiin URLs
urlpatterns = [
    path("logout/", views.LogOut, name="logout"),
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("sign-up", views.sign_up, name="sign-up"),
    path("about-us", views.about_us, name="about-us"),
    path("locator", views.locator, name="locator"),
    path("", include("django.contrib.auth.urls")),
    
    # Checkout routes
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout_view, name='checkout'),

    path('clear-cart/', clear_cart, name='clear_cart'),
]
