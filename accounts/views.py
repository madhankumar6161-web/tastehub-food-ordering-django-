"""
accounts/views.py
Login, logout, registration and profile update views.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ProfileForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


def register_view(request):
    """Handles new customer sign-up."""
    if request.user.is_authenticated:
        return redirect('menu:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login right after registering
            messages.success(request, f"Welcome aboard, {user.username}! Your account is ready.")
            return redirect('menu:home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You've been logged out. See you again soon!")
    return redirect('menu:home')


@login_required
def profile_view(request):
    """Lets a logged-in customer view/update their delivery details."""
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)

    # Show recent order history on the same page
    orders = request.user.orders.all().order_by('-created_at')[:10]
    return render(request, 'accounts/profile.html', {'form': form, 'orders': orders})
