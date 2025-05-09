from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from .models import Bread, Protein, Cheese, Vegetable, Condiment, Extra, Sandwich
from .forms import SandwichForm
# Create your views here.
def home(request):
    return render(request, 'main/home.html')


class SandwichCreateView(CreateView):
    model = Sandwich
    form_class = SandwichForm
    template_name = 'customizeSandwich.html'
    success_url = reverse_lazy('cart')
    
    def form_valid(self, form):
        sandwich = form.save()
        
        if 'cart' not in self.request.session:
            self.request.session['cart'] = []
        
        cart = self.request.session['cart']
        cart.append({
            'sandwich_id': sandwich.id,
            'quantity': 1
        })
        self.request.session['cart'] = cart
        
        return redirect(self.success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add pricing information for display in the form
        context['breads'] = Bread.objects.filter(available=True)
        context['proteins'] = Protein.objects.filter(available=True)
        context['cheeses'] = Cheese.objects.filter(available=True)
        context['vegetables'] = Vegetable.objects.filter(available=True)
        context['condiments'] = Condiment.objects.filter(available=True)
        context['extras'] = Extra.objects.filter(available=True)
        return context





 