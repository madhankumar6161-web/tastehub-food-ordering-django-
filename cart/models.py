"""
cart/models.py
A database-backed cart so it demonstrates real relational modelling
(Cart -> CartItem -> MenuItem) instead of only using the session.
Works for both guests (tracked by session_key) and logged-in users.
"""
from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem


class Cart(models.Model):
    """One active cart per user (or per anonymous session)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_checked_out = models.BooleanField(default=False)

    def __str__(self):
        owner = self.user.username if self.user else f"guest:{self.session_key}"
        return f"Cart({owner})"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """A single line item inside a cart: which dish + how many."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'menu_item')  # adding same dish again just bumps quantity

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

    @property
    def subtotal(self):
        return self.menu_item.price * self.quantity
