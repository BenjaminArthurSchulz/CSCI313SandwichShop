from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        
        if commit:
            # Try to get the profile, if it doesn't exist, create it
            try:
                user_profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                user_profile = UserProfile.objects.create(user=user)
            
            # Save the profile fields from the form
            user_profile.phone_number = self.cleaned_data.get('phone_number', '')
            user_profile.address = self.cleaned_data.get('address', '')
            user_profile.save()
            
        return user

# Checkout form

class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=255, widget=forms.Textarea(attrs={'rows': 3}))
    payment_method = forms.ChoiceField(
        choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')],
        widget=forms.RadioSelect
    )




