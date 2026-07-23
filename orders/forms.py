"""
orders/forms.py
Checkout form: delivery address + payment method selection.
"""
from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone_number', 'address_line', 'city', 'pincode',
                  'delivery_notes', 'payment_method']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 98765 43210'}),
            'address_line': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House no, street, landmark'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
            'delivery_notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Ring the bell twice (optional)'}),
            'payment_method': forms.RadioSelect,
        }
