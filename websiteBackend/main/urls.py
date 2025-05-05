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
