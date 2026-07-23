from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/<str:order_number>/', views.payment_view, name='payment'),
    path('payment/<str:order_number>/confirm/', views.confirm_payment, name='confirm_payment'),
    path('track/<str:order_number>/', views.tracking_view, name='tracking'),
    path('my-orders/', views.my_orders_view, name='my_orders'),
]
