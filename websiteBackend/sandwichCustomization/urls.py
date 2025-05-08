from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('customize/', views.SandwichCreateView.as_view(), name='customize_sandwich'),
]