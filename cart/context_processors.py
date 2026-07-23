"""
cart/context_processors.py
Injects `cart_item_count` into EVERY template's context (used for the
little badge on the navbar cart icon), so we don't repeat this query
in every single view.
"""
from .cart_utils import get_current_cart


def cart_summary(request):
    try:
        cart = get_current_cart(request)
        return {'cart_item_count': cart.total_items, 'cart_total_price': cart.total_price}
    except Exception:
        # Fails gracefully during admin requests, management commands, etc.
        return {'cart_item_count': 0, 'cart_total_price': 0}
