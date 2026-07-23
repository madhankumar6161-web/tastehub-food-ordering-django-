"""
orders/admin.py
This is where the restaurant manager updates the LIVE STATUS of active
orders (Order Placed -> Preparing -> Out for Delivery -> Delivered).
Changing `status` here automatically writes a new OrderStatusLog row,
which is what powers the customer-facing tracking timeline.
"""
from django.contrib import admin
from .models import Order, OrderItem, OrderStatusLog


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('menu_item', 'item_name', 'item_price', 'quantity')
    can_delete = False


class OrderStatusLogInline(admin.TabularInline):
    model = OrderStatusLog
    extra = 0
    readonly_fields = ('status', 'note', 'changed_at')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'status', 'payment_method',
                     'payment_status', 'total_amount', 'created_at')
    list_editable = ('status',)  # manager can update status right from the list view
    list_filter = ('status', 'payment_method', 'payment_status')
    search_fields = ('order_number', 'full_name', 'phone_number')
    readonly_fields = ('order_number', 'subtotal', 'total_amount', 'created_at', 'updated_at')
    inlines = [OrderItemInline, OrderStatusLogInline]

    def save_model(self, request, obj, form, change):
        """Whenever staff changes `status` in admin, log it for the tracking timeline."""
        if change and 'status' in form.changed_data:
            super().save_model(request, obj, form, change)
            OrderStatusLog.objects.create(
                order=obj, status=obj.status,
                note=f"Status updated to '{obj.get_status_display()}' by {request.user.username}."
            )
        else:
            super().save_model(request, obj, form, change)
