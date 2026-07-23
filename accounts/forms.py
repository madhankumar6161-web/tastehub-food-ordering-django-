"""
accounts/forms.py
Registration & profile forms built on Django's built-in UserCreationForm.
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # profile row already exists via the post_save signal; just fill it in
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.phone_number = self.cleaned_data['phone_number']
            profile.save()
            user.email = self.cleaned_data['email']
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    """Used on checkout / profile page to capture delivery details."""
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address_line', 'city', 'pincode']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 98765 43210'}),
            'address_line': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House no, Street, Landmark'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
        }
