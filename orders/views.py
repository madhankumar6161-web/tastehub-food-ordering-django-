"""
orders/views.py
Checkout -> Payment (simulated) -> Order Tracking flow.
"""
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from cart.cart_utils import get_current_cart
from .models import Order, OrderItem, OrderStatusLog
from .forms import CheckoutForm

DELIVERY_FEE = Decimal('40.00')


def checkout_view(request):
    """
    Step 1: shows order summary + delivery address form + payment method choice.
    Redirects back to cart if it's empty.
    """
    cart = get_current_cart(request)
    if cart.total_items == 0:
        messages.warning(request, "Your cart is empty. Add some delicious food first!")
        return redirect('menu:menu_list')

    initial = {}
    if request.user.is_authenticated:
        profile = request.user.profile
        initial = {
            'full_name': request.user.get_full_name() or request.user.username,
            'phone_number': profile.phone_number,
            'address_line': profile.address_line,
            'city': profile.city,
            'pincode': profile.pincode,
        }

    if request.method == 'POST':
        form = CheckoutForm(request.POST, initial=initial)
        if form.is_valid():
            # Create the Order now (payment still 'pending'); we finalize
            # payment status on the next (simulated payment) step.
            order = form.save(commit=False)
            order.user = request.user if request.user.is_authenticated else None
            order.subtotal = cart.total_price
            order.delivery_fee = DELIVERY_FEE
            order.total_amount = cart.total_price + DELIVERY_FEE
            order.save()

            for cart_item in cart.items.select_related('menu_item'):
                OrderItem.objects.create(
                    order=order,
                    menu_item=cart_item.menu_item,
                    item_name=cart_item.menu_item.name,
                    item_price=cart_item.menu_item.price,
                    quantity=cart_item.quantity,
                )

            OrderStatusLog.objects.create(order=order, status='placed', note='Order placed by customer.')

            # empty the cart now that it has been converted into an order
            cart.items.all().delete()
            cart.is_checked_out = True
            cart.save()

            return redirect('orders:payment', order_number=order.order_number)
    else:
        form = CheckoutForm(initial=initial)

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart,
        'delivery_fee': DELIVERY_FEE,
        'grand_total': cart.total_price + DELIVERY_FEE,
    })


def payment_view(request, order_number):
    """
    Step 2: simulated payment screen.
    - If payment_method == 'cod' -> mark as confirmed immediately (no gateway needed).
    - If 'card' / 'upi' -> shows a mock gateway UI (Uiverse-style spinner + fake
      card form). JS calls `confirm_payment` after a short delay to "process" it.
    """
    order = get_object_or_404(Order, order_number=order_number)

    if order.payment_method == 'cod' and order.payment_status == 'pending':
        order.payment_status = 'pending'  # stays pending until delivery, by design
        order.status = 'confirmed'
        order.save()
        OrderStatusLog.objects.create(order=order, status='confirmed', note='Cash on Delivery order confirmed.')
        return redirect('orders:tracking', order_number=order.order_number)

    return render(request, 'orders/payment.html', {'order': order})


@require_POST
def confirm_payment(request, order_number):
    """
    AJAX endpoint hit by payment.html's JS after the simulated gateway
    'processes' the card/UPI details. Always succeeds (this is a portfolio
    simulation, not a real gateway) and advances the order status.
    """
    order = get_object_or_404(Order, order_number=order_number)
    order.payment_status = 'paid'
    order.status = 'confirmed'
    order.save()
    OrderStatusLog.objects.create(order=order, status='confirmed', note='Payment received. Order confirmed.')

    return JsonResponse({
        'success': True,
        'redirect_url': f'/orders/track/{order.order_number}/',
    })


def tracking_view(request, order_number):
    """Step 3: visual timeline — Order Placed -> Preparing -> Out for Delivery -> Delivered."""
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'orders/tracking.html', {'order': order})


@login_required
def my_orders_view(request):
    """List of the logged-in customer's past & active orders."""
    orders = request.user.orders.all()
    return render(request, 'orders/my_orders.html', {'orders': orders})
