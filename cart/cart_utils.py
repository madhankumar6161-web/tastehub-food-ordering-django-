"""
cart/cart_utils.py
Helper to fetch-or-create the correct Cart for the current request,
whether the visitor is logged in or browsing as a guest.
"""
from .models import Cart


def get_current_cart(request):
    """
    Returns the Cart tied to the logged-in user, or to the guest's
    session key if anonymous. Creates one on first use.
    """
    if not request.session.session_key:
        request.session.create()

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, is_checked_out=False)
        return cart

    cart, _ = Cart.objects.get_or_create(
        session_key=request.session.session_key,
        user=None,
        is_checked_out=False,
    )
    return cart


def merge_guest_cart_into_user(request, user):
    """
    Call this right after login: folds any items the guest added
    before logging in into their permanent account cart.
    """
    session_key = request.session.session_key
    if not session_key:
        return
    guest_cart = Cart.objects.filter(session_key=session_key, user=None, is_checked_out=False).first()
    if not guest_cart:
        return
    user_cart, _ = Cart.objects.get_or_create(user=user, is_checked_out=False)
    for item in guest_cart.items.all():
        existing = user_cart.items.filter(menu_item=item.menu_item).first()
        if existing:
            existing.quantity += item.quantity
            existing.save()
        else:
            item.cart = user_cart
            item.save()
    guest_cart.delete()
