"""
menu/management/commands/seed_menu.py

Run with:  python manage.py seed_menu

Populates the database with realistic demo Categories & MenuItems
(using Unsplash image URLs as placeholders) so the site looks fully
populated immediately after setup — no manual data entry needed.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from menu.models import Category, MenuItem


CATEGORIES = [
    ("Italian", "bi-egg-fried"),
    ("Asian", "bi-egg"),
    ("Fast Food", "bi-cup-straw"),
    ("Desserts", "bi-cake2"),
    ("Beverages", "bi-cup-hot"),
]

# (category, name, description, price, dietary_type, image_url, featured)
ITEMS = [
    ("Italian", "Margherita Pizza",
     "Classic wood-fired pizza with San Marzano tomato sauce, fresh mozzarella, and basil.",
     299, "veg", "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=700&q=80", True),
    ("Italian", "Creamy Alfredo Pasta",
     "Fettuccine tossed in a rich parmesan cream sauce with garlic and cracked pepper.",
     349, "veg", "https://images.unsplash.com/photo-1645112411341-6c4fd023714a?w=700&q=80", False),
    ("Italian", "Pepperoni Pizza",
     "A generous layer of spicy pepperoni over bubbling mozzarella and tomato sauce.",
     379, "non_veg", "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=700&q=80", True),
    ("Italian", "Bruschetta",
     "Toasted baguette slices topped with diced tomato, garlic, basil and olive oil.",
     199, "vegan", "https://images.unsplash.com/photo-1572695157366-5e585ab2b69f?w=700&q=80", False),

    ("Asian", "Chicken Ramen",
     "Slow-simmered pork broth with noodles, soft-boiled egg, scallions and chicken slices.",
     329, "non_veg", "https://images.unsplash.com/photo-1591814468924-caf88d1232e1?w=700&q=80", True),
    ("Asian", "Vegetable Spring Rolls",
     "Crispy fried rolls stuffed with cabbage, carrot and glass noodles, served with sweet chili.",
     179, "vegan", "https://images.unsplash.com/photo-1544025162-d76694265947?w=700&q=80", False),
    ("Asian", "Kung Pao Chicken",
     "Wok-tossed chicken with peanuts, dried chilies and a tangy Sichuan sauce.",
     359, "non_veg", "https://images.unsplash.com/photo-1626200419199-391ae4be7a41?w=700&q=80", False),
    ("Asian", "Vegetable Fried Rice",
     "Wok-fried rice with mixed vegetables, soy sauce and scallions.",
     229, "veg", "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=700&q=80", False),

    ("Fast Food", "Classic Cheeseburger",
     "Grilled beef patty, cheddar cheese, lettuce, tomato and house sauce in a brioche bun.",
     259, "non_veg", "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=700&q=80", True),
    ("Fast Food", "Crispy Chicken Burger",
     "Buttermilk-fried chicken breast, slaw and spicy mayo in a toasted bun.",
     279, "non_veg", "https://images.unsplash.com/photo-1606755962773-d324e0a13086?w=700&q=80", False),
    ("Fast Food", "Loaded French Fries",
     "Crispy fries loaded with cheese sauce, jalapeños and a smoky drizzle.",
     189, "veg", "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=700&q=80", False),
    ("Fast Food", "Veggie Burger",
     "A grilled plant-based patty with lettuce, tomato and vegan mayo.",
     239, "vegan", "https://images.unsplash.com/photo-1520072959219-c595dc870360?w=700&q=80", False),

    ("Desserts", "Chocolate Lava Cake",
     "Warm chocolate cake with a molten center, served with vanilla ice cream.",
     199, "veg", "https://images.unsplash.com/photo-1624353365286-3f8d62daad51?w=700&q=80", True),
    ("Desserts", "New York Cheesecake",
     "Creamy baked cheesecake on a buttery biscuit base, topped with berry compote.",
     229, "veg", "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=700&q=80", False),

    ("Beverages", "Cold Brew Coffee",
     "Smooth, slow-steeped cold brew served over ice.",
     149, "vegan", "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=700&q=80", False),
    ("Beverages", "Fresh Mango Smoothie",
     "Ripe mango blended with yogurt and a hint of honey.",
     169, "veg", "https://images.unsplash.com/photo-1546173159-315724a31696?w=700&q=80", True),
]


class Command(BaseCommand):
    help = "Seeds the database with demo categories and menu items."

    def handle(self, *args, **options):
        cat_objs = {}
        for order, (name, icon) in enumerate(CATEGORIES):
            cat, _ = Category.objects.get_or_create(
                name=name, defaults={'slug': slugify(name), 'icon_class': icon, 'order': order}
            )
            cat_objs[name] = cat
        self.stdout.write(self.style.SUCCESS(f"Categories ready: {len(cat_objs)}"))

        created_count = 0
        for cat_name, name, desc, price, diet, image_url, featured in ITEMS:
            _, created = MenuItem.objects.get_or_create(
                slug=slugify(name),
                defaults={
                    'category': cat_objs[cat_name],
                    'name': name,
                    'description': desc,
                    'price': price,
                    'dietary_type': diet,
                    'image_url': image_url,
                    'is_featured': featured,
                    'is_available': True,
                }
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Menu items created: {created_count} (of {len(ITEMS)} total defined)"))
        self.stdout.write(self.style.SUCCESS("Seeding complete! Run the server and visit the homepage."))
