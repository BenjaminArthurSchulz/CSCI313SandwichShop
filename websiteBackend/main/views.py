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

def locator(request):
    stores = [
        {"name": "BLT Sandwich Shop, Fargo", "address": "3220 39th St S, Fargo, ND"},
        {"name": "BLT Sandwich Shop, Jamestown", "address": "1921 8th Ave SW, Jamestown, ND"},
        {"name": "BLT Sandwich Shop, Detroit Lakes", "address": "1302 Washington Ave, Detroit Lakes, MN"},
        {"name": "BLT Sandwich Shop, Bemidji", "address": "1008 Paul Bunyan Dr NW, Bemidji, MN"},
    ]
    return render(request, 'main/locator.html', {'stores': stores})



# Checkout views
@login_required
def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    total_price = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total_price += product.price * quantity

    discount = 0
    if request.method == 'POST':
        if 'apply_coupon' in request.POST:
            coupon_form = CouponForm(request.POST)
            if coupon_form.is_valid():
                try:
                    coupon = Coupon.objects.get(code=coupon_form.cleaned_data['code'])
                    if coupon.is_valid():
                        discount = coupon.discount_amount
                        request.session['coupon'] = coupon.code
                    else:
                        coupon_form.add_error('code', 'Invalid or expired coupon.')
                except Coupon.DoesNotExist:
                    coupon_form.add_error('code', 'Coupon does not exist.')
        elif 'checkout' in request.POST:
            form = CheckoutForm(request.POST)
            if form.is_valid():
                coupon_code = request.session.get('coupon')
                if coupon_code:
                    try:
                        coupon = Coupon.objects.get(code=coupon_code)
                        if coupon.is_valid():
                            discount = coupon.discount_amount
                        else:
                            del request.session['coupon']
                    except Coupon.DoesNotExist:
                        del request.session['coupon']

                order = Order.objects.create(user=request.user, total_price=total_price - discount)
                for product_id, quantity in cart.items():
                    product = Product.objects.get(id=product_id)
                    OrderItem.objects.create(order=order, product=product, quantity=quantity)

                request.session.pop('cart', None)
                request.session.pop('coupon', None)
                return render(request, 'order_confirmation.html', {'order': order})

    else:
        form = CheckoutForm()
        coupon_form = CouponForm()

    total_price -= discount
    return render(request, 'checkout.html', {
        'form': form,
        'coupon_form': coupon_form,
        'total_price': total_price,
        'discount': discount
    })