"""
menu/admin.py
This IS the "Secure Admin Panel" requirement: Django's built-in admin,
customized so restaurant managers can add/edit dishes, change prices,
and toggle availability without touching code. Only staff accounts
(is_staff=True) can log in at /admin/.
"""
from django.contrib import admin
from .models import Category, MenuItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'dietary_type', 'is_available', 'is_featured')
    list_editable = ('price', 'is_available', 'is_featured')  # quick inline edits, no need to open each item
    list_filter = ('category', 'dietary_type', 'is_available', 'is_featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 25
