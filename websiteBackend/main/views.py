from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from sandwichCustomization.models import Bread, Protein, Cheese, Vegetable, Condiment, Extra
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
def cart_view(request):
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}

    cart_items = []
    total_price = 0

    for cart_key, item in cart.items():
        subtotal = item['price'] * item['quantity']
        total_price += subtotal
        cart_items.append({
            'description': item['description'],
            'price': item['price'],
            'quantity': item['quantity'],
            'subtotal': subtotal,
        })

    return render(request, 'checkout/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        # Collect selected options
        bread_id = request.POST.get('bread')
        protein_ids = request.POST.getlist('proteins')
        cheese_ids = request.POST.getlist('cheeses')
        vegetable_ids = request.POST.getlist('vegetables')
        condiment_ids = request.POST.getlist('condiments')
        extra_ids = request.POST.getlist('extras')
        toasted = 'toasted' in request.POST

        # Initialize cart item details
        sandwich_desc = []
        total_price = 0

        if bread_id:
            bread = Bread.objects.get(id=bread_id)
            sandwich_desc.append(f"Bread: {bread.name}")
            total_price += bread.price

        for pid in protein_ids:
            protein = Protein.objects.get(id=pid)
            sandwich_desc.append(f"Protein: {protein.name}")
            total_price += protein.price

        for cid in cheese_ids:
            cheese = Cheese.objects.get(id=cid)
            sandwich_desc.append(f"Cheese: {cheese.name}")
            total_price += cheese.price

        for vid in vegetable_ids:
            vegetable = Vegetable.objects.get(id=vid)
            sandwich_desc.append(f"Vegetable: {vegetable.name}")
            total_price += vegetable.price

        for condid in condiment_ids:
            condiment = Condiment.objects.get(id=condid)
            sandwich_desc.append(f"Condiment: {condiment.name}")
            total_price += condiment.price

        for exid in extra_ids:
            extra = Extra.objects.get(id=exid)
            sandwich_desc.append(f"Extra: {extra.name}")
            total_price += extra.price

        if toasted:
            sandwich_desc.append("Toasted")

        # Store in cart (session)
        cart = request.session.get('cart', {})
        if not isinstance(cart, dict):
            cart = {}  # 💥 Ensure it's a dict

        from uuid import uuid4
        cart_key = str(uuid4())

        cart[cart_key] = {
            'description': sandwich_desc,
            'price': float(total_price),
            'quantity': 1,
        }

        request.session['cart'] = cart

        return redirect('cart')

    return redirect('customize_sandwich')

@login_required
def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    total_price = 0
    for cart_key, item in cart.items():
        total_price += item['price'] * item['quantity']

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

                # Create the order with the total price
                order = Order.objects.create(user=request.user, total_price=total_price - discount)

                # Save each custom sandwich as an OrderItem (adjust as needed)
                for cart_key, item in cart.items():
                    # Here, we can create OrderItem with description
                    OrderItem.objects.create(
                        order=order,
                        description="\n".join(item['description']),
                        price=item['price'],
                        quantity=item['quantity']
                    )

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

def clear_cart(request):
    # Clear the cart from the session
    request.session.pop('cart', None)  # This removes the cart from the session
    return redirect('cart')  # Redirect to the cart view or another page