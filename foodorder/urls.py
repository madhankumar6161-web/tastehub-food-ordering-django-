"""
Root URL configuration.
Delegates to each app's own urls.py to keep things modular.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),           # Home + Menu browsing
    path('accounts/', include('accounts.urls')),  # Login/Register/Profile
    path('cart/', include('cart.urls')),       # Cart add/remove/update
    path('orders/', include('orders.urls')),   # Checkout/Payment/Tracking
]

# Serve uploaded food images during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
