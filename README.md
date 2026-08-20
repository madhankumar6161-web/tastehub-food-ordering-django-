# TasteHub — Food Ordering System (Django Portfolio Project)

A full-stack food ordering web app: browse a categorized menu, add items to
a live cart, check out with a simulated payment gateway, and track your
order through a live status timeline. Built with **Django** + **Bootstrap 5**
+ **Anime.js** + **Swiper.js**.

---

## 1. Feature Checklist

| Requirement | Where it lives |
|---|---|
| Dynamic categorized menu (cuisine + dietary filters) | `menu` app, `templates/menu/menu_list.html` |
| Add to cart, live totals, quantity control | `cart` app (AJAX), `templates/cart/cart.html`, `static/js/cart.js` |
| Checkout (address + summary) | `orders` app, `templates/orders/checkout.html` |
| Simulated payment (Card / UPI / Cash on Delivery) | `orders/views.py: payment_view`, `templates/orders/payment.html` |
| Order tracking timeline | `orders/views.py: tracking_view`, `templates/orders/tracking.html` |
| Secure admin panel (menu + live order status) | Django Admin, customized in `menu/admin.py` & `orders/admin.py` |
| Anime.js micro-interactions ("flying" add-to-cart, card entrance) | `static/js/animations.js` |
| Swiper "Popular Dishes" carousel | `templates/menu/home.html` |
| Bootstrap 5 responsive layout, forms, modals | `templates/base.html` + all templates |
| Uiverse-style buttons/spinner | `.btn-place-order`, `.uiverse-spinner` in `static/css/style.css` |

---

## 2. Project Architecture (Folder Structure)

```
foodorder/                         ← project root 
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── db.sqlite3                     ← auto-created on first migrate (SQLite default)
│
├── foodorder/                     ← Django project config
│   ├── __init__.py
│   ├── settings.py                ← SQLite by default; MySQL block commented in
│   ├── urls.py                    ← root URL router -> includes each app
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                      ← users, profile, auth
│   ├── models.py                  ← UserProfile (1-1 with Django's User)
│   ├── forms.py                   ← RegisterForm, ProfileForm
│   ├── views.py                   ← login/register/logout/profile
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
│
├── menu/                          ← restaurant menu
│   ├── models.py                  ← Category, MenuItem
│   ├── views.py                   ← home, menu_list, item_detail
│   ├── urls.py
│   ├── admin.py                   ← THIS is the manager's "edit menu" panel
│   ├── migrations/
│   └── management/commands/
│       └── seed_menu.py           ← `python manage.py seed_menu` demo data
│
├── cart/                          ← shopping cart (DB-backed, guest + user)
│   ├── models.py                  ← Cart, CartItem
│   ├── cart_utils.py              ← get_current_cart(), merge on login
│   ├── context_processors.py      ← navbar cart-count on every page
│   ├── views.py                   ← AJAX add/update/remove
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
│
├── orders/                        ← checkout, payment, tracking
│   ├── models.py                  ← Order, OrderItem, OrderStatusLog
│   ├── forms.py                   ← CheckoutForm
│   ├── views.py                   ← checkout / payment / confirm_payment / tracking
│   ├── urls.py
│   ├── admin.py                   ← manager updates live order status HERE
│   └── migrations/
│
├── templates/                     ← all HTML (project-level, shared by all apps)
│   ├── base.html                  ← navbar, footer, CDN libs (Bootstrap/Swiper/Anime)
│   ├── menu/
│   │   ├── home.html
│   │   ├── menu_list.html
│   │   └── item_detail.html
│   ├── cart/
│   │   └── cart.html
│   ├── orders/
│   │   ├── checkout.html
│   │   ├── payment.html
│   │   ├── tracking.html
│   │   └── my_orders.html
│   └── accounts/
│       ├── login.html
│       ├── register.html
│       └── profile.html
│
├── static/                        ← CSS/JS (source files, served in DEBUG mode)
│   ├── css/
│   │   └── style.css              ← palette, cards, buttons, timeline, spinner
│   └── js/
│       ├── main.js                ← toasts, active-nav-link, alert auto-dismiss
│       ├── cart.js                ← fetch()-based add/update/remove
│       └── animations.js          ← Anime.js flying-cart + card entrance
│
└── media/                         ← uploaded images land here (via admin panel)
    └── food_images/
