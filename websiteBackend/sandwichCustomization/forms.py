

from django import forms
from .models import Bread, Protein, Cheese, Vegetable, Condiment, Extra, Sandwich


class SandwichForm(forms.ModelForm):
    bread = forms.ModelChoiceField(
        queryset=Bread.objects.filter(available=True),
        widget=forms.RadioSelect,
        empty_label=None
    )
    proteins = forms.ModelMultipleChoiceField(
        queryset=Protein.objects.filter(available=True),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    cheeses = forms.ModelMultipleChoiceField(
        queryset=Cheese.objects.filter(available=True),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    vegetables = forms.ModelMultipleChoiceField(
        queryset=Vegetable.objects.filter(available=True),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    condiments = forms.ModelMultipleChoiceField(
        queryset=Condiment.objects.filter(available=True),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    extras = forms.ModelMultipleChoiceField(
        queryset=Extra.objects.filter(available=True),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    toasted = forms.BooleanField(required=False)
    
    class Meta:
        model = Sandwich
        fields = ['bread', 'proteins', 'cheeses', 'vegetables', 'condiments', 'extras', 'toasted']


