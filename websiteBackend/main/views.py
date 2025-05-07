from django.shortcuts import redirect, render

from main.models import UserProfile
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.



def home(request):
    return render(request, "main/home.html")

def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            UserProfile.objects.get_or_create(user=user)

            login(request, user)
            return redirect("/home")
    else:
        form = RegisterForm()
    return render(request, "registration/sign_up.html", {"form": form})

from django.db import close_old_connections
close_old_connections()

def LogOut(request):
    logout(request)
    return redirect("/login/")



