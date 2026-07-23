"""
cart/views.py
AJAX-friendly endpoints so the frontend cart can add/remove/update
items and get a live-updating total WITHOUT a full page reload
(pairs with cart.js + Anime.js "flying item" animation).
"""
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from menu.models import MenuItem
from .cart_utils import get_current_cart
from .models import CartItem


def cart_detail_view(request):
    """Full cart page: list of items, quantity steppers, live total, 'Proceed to Checkout' button."""
    cart = get_current_cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


@require_POST
def add_to_cart(request, item_id):
    """
    AJAX endpoint: POST /cart/add/<item_id>/
    Adds one unit of a dish to the cart (or increments quantity if already in cart).
    Returns updated totals as JSON so the frontend can update the badge instantly.
    """
    menu_item = get_object_or_404(MenuItem, id=item_id, is_available=True)
    cart = get_current_cart(request)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({
        'success': True,
        'message': f'{menu_item.name} added to cart',
        'cart_item_count': cart.total_items,
        'cart_total_price': str(cart.total_price),
    })


@require_POST
def update_cart_item(request, item_id):
    """
    AJAX endpoint: POST /cart/update/<item_id>/  body: {"action": "increase"|"decrease"}
    Adjusts quantity of a specific cart line, removing it if it drops to 0.
    """
    data = json.loads(request.body or '{}')
    action = data.get('action')

    cart = get_current_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()

    return JsonResponse({
        'success': True,
        'cart_item_count': cart.total_items,
        'cart_total_price': str(cart.total_price),
    })


@require_POST
def remove_from_cart(request, item_id):
    """AJAX endpoint: POST /cart/remove/<item_id>/ - deletes a line entirely."""
    cart = get_current_cart(request)
    CartItem.objects.filter(id=item_id, cart=cart).delete()
    return JsonResponse({
        'success': True,
        'cart_item_count': cart.total_items,
        'cart_total_price': str(cart.total_price),
    })
