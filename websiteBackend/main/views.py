from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from .forms import CheckoutForm
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

def about_us(request):
    return render(request, "main/aboutUs.html")


# Checkout views
@login_required
def cart_view(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}
    cart = request.session['cart']
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total_price = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total_price += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    cart[str(product.id)] = cart.get(str(product.id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

@login_required
def checkout_view(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cart = request.session.get('cart', {})
            if not cart:
                return redirect('cart')

            order = Order.objects.create(user=request.user, total_price=0)
            total_price = 0

            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                subtotal = product.price * quantity
                total_price += subtotal
                OrderItem.objects.create(order=order, product=product, quantity=quantity)

            order.total_price = total_price
            order.save()

            request.session.pop('cart', None)  # Clear the cart
            return render(request, 'order_confirmation.html', {'order': order})
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form})
