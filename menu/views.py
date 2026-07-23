"""
menu/views.py
Home page (hero + featured carousel) and the full menu grid with
category / dietary filters.
"""
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, MenuItem


def home_view(request):
    """Landing page: hero banner, Swiper carousel of featured dishes, quick categories."""
    featured_items = MenuItem.objects.filter(is_featured=True, is_available=True)[:8]
    categories = Category.objects.all()
    return render(request, 'menu/home.html', {
        'featured_items': featured_items,
        'categories': categories,
    })


def menu_list_view(request):
    """
    Full menu grid. Supports query params:
      ?category=<slug>   filter by cuisine/category
      ?diet=veg|vegan|non_veg   filter by dietary preference
      ?q=<text>          simple search across name/description
    """
    items = MenuItem.objects.filter(is_available=True).select_related('category')
    categories = Category.objects.all()

    selected_category = request.GET.get('category', '')
    selected_diet = request.GET.get('diet', '')
    query = request.GET.get('q', '').strip()

    if selected_category:
        items = items.filter(category__slug=selected_category)
    if selected_diet:
        items = items.filter(dietary_type=selected_diet)
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'menu/menu_list.html', {
        'items': items,
        'categories': categories,
        'selected_category': selected_category,
        'selected_diet': selected_diet,
        'query': query,
    })


def item_detail_view(request, slug):
    """Single dish detail page — useful for a 'quick view' modal or its own page."""
    item = get_object_or_404(MenuItem, slug=slug, is_available=True)
    related_items = MenuItem.objects.filter(category=item.category, is_available=True).exclude(id=item.id)[:4]
    return render(request, 'menu/item_detail.html', {'item': item, 'related_items': related_items})
