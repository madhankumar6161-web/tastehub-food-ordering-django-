from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'city', 'is_staff_manager')
    list_filter = ('is_staff_manager', 'city')
    search_fields = ('user__username', 'phone_number')
