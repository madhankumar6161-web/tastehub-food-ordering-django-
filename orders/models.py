"""
orders/models.py
Order        -> a placed order (address, payment method, current status)
OrderItem    -> snapshot of each dish + price + quantity AT THE TIME of order
                (never references live cart, so price changes later don't
                rewrite history)
OrderStatusLog -> an audit trail of every status change, which powers the
                   "real-time" tracking timeline UI.
"""
import uuid
from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem


class Order(models.Model):

    STATUS_CHOICES = [
        ('placed', 'Order Placed'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash / Pay on Delivery'),
        ('card', 'Credit / Debit Card (Simulated)'),
        ('upi', 'UPI (Simulated)'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    # Human-friendly public order number shown to the customer, e.g. FO-8F3A21
    order_number = models.CharField(max_length=12, unique=True, editable=False, blank=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')

    # Delivery details captured at checkout (kept even if the user later edits their profile)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    delivery_notes = models.CharField(max_length=255, blank=True)

    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default='cod')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=40)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='placed')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"FO-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

    # Ordered list of stages used to render the progress timeline
    TRACKING_STAGES = ['placed', 'confirmed', 'preparing', 'out_for_delivery', 'delivered']

    @property
    def current_stage_index(self):
        """Returns index of current status within TRACKING_STAGES (used to fill progress bar)."""
        try:
            return self.TRACKING_STAGES.index(self.status)
        except ValueError:
            return -1  # e.g. 'cancelled' - handled separately in template


class OrderItem(models.Model):
    """Snapshot line item: dish name/price frozen at the moment of ordering."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True, related_name='order_items')
    item_name = models.CharField(max_length=120)       # frozen copy, survives menu item edits/deletion
    item_price = models.DecimalField(max_digits=8, decimal_places=2)  # frozen price at order time
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item_name}"

    @property
    def subtotal(self):
        return self.item_price * self.quantity


class OrderStatusLog(models.Model):
    """
    Audit trail: every time the restaurant manager (or a simulator script)
    changes an order's status, a row is added here. The tracking page
    reads this to show a timestamped timeline.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_logs')
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    note = models.CharField(max_length=255, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['changed_at']

    def __str__(self):
        return f"{self.order.order_number} -> {self.status}"
