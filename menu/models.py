"""
menu/models.py
Category  -> groups items (Italian, Asian, Fast Food, Desserts, Beverages...)
MenuItem  -> the actual dish, with price, dietary tag, availability toggle etc.
"""
from django.db import models
from django.urls import reverse


class Category(models.Model):
    """A cuisine / section grouping, e.g. Italian, Asian, Fast Food, Desserts."""
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    icon_class = models.CharField(
        max_length=50, blank=True,
        help_text="Optional Bootstrap Icons class, e.g. 'bi-egg-fried'"
    )
    order = models.PositiveIntegerField(default=0, help_text="Controls display order on the menu page")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """A single dish available for order."""

    DIETARY_CHOICES = [
        ('veg', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('non_veg', 'Non-Vegetarian'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Price in INR")

    # Placeholder-friendly: either upload to /media/food_images/ or paste an
    # Unsplash/Pexels URL and use `image_url` in templates as a fallback.
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    image_url = models.URLField(
        blank=True,
        help_text="Fallback image URL (e.g. an Unsplash link) if no file is uploaded."
    )

    dietary_type = models.CharField(max_length=10, choices=DIETARY_CHOICES, default='veg')
    is_available = models.BooleanField(default=True, help_text="Uncheck to hide from the live menu (out of stock)")
    is_featured = models.BooleanField(default=False, help_text="Show in the homepage 'Popular Dishes' carousel")
    spice_level = models.PositiveSmallIntegerField(default=0, help_text="0 = none, 3 = very spicy")
    prep_time_minutes = models.PositiveIntegerField(default=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category__order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('menu:item_detail', kwargs={'slug': self.slug})

    @property
    def display_image(self):
        """Return uploaded image if present, else the fallback URL, else a generic placeholder."""
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&q=80'
