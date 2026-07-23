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
foodorder/                         ← project root (zip this whole folder)
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
```

---

## 3. Step-by-Step VS Code Setup Guide

### Step 1 — Open the project
1. Unzip the project folder.
2. Open VS Code → `File > Open Folder...` → select the unzipped `foodorder` folder.
3. Install the **Python** extension (Microsoft) if you haven't already.

### Step 2 — Create & activate a virtual environment
Open the VS Code integrated terminal (`` Ctrl+` ``) and run:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal prompt.
In VS Code, also select this interpreter: `Ctrl+Shift+P` → *Python: Select Interpreter* → choose the one inside `venv`.

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run migrations (creates the database tables)
By default the project uses **SQLite** — zero configuration needed.
```bash
python manage.py migrate
```

### Step 5 — Load demo menu data (optional but recommended)
This populates 5 categories and 16 dishes with real Unsplash photos, prices,
and descriptions, so the site looks complete immediately:
```bash
python manage.py seed_menu
```

### Step 6 — Create an admin (restaurant manager) account
```bash
python manage.py createsuperuser
```
Follow the prompts to set a username, email, and password.

### Step 7 — Run the development server
```bash
python manage.py runserver
```
Visit **http://127.0.0.1:8000/** for the customer site, and
**http://127.0.0.1:8000/admin/** to log in as the restaurant manager.

### Step 8 (Optional) — Switch to MySQL
1. Install MySQL Server and create a database:
   ```sql
   CREATE DATABASE foodorder_db CHARACTER SET utf8mb4;
   ```
2. Install the MySQL driver:
   ```bash
   pip install mysqlclient
   ```
   > On Windows, if `mysqlclient` fails to build, install the prebuilt wheel
   > matching your Python version from https://pypi.org/project/mysqlclient/
   > or use `pip install pymysql` and add these two lines to the **top** of
   > `foodorder/__init__.py`: `import pymysql; pymysql.install_as_MySQLdb()`
3. Open `foodorder/settings.py`, comment out the `DATABASES` (SQLite) block,
   and uncomment the MySQL block right below it. Fill in your MySQL
   username/password (or set them as environment variables `DB_NAME`,
   `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`).
4. Re-run `python manage.py migrate`, `python manage.py seed_menu`, and
   `python manage.py createsuperuser`.

---

## 4. Using the Site

### As a customer
1. Browse **Menu**, filter by category or dietary type.
2. Click **Add** on any dish — watch the flying-to-cart animation and the
   navbar badge update instantly (no page reload).
3. Open the **Cart** icon, adjust quantities, then **Proceed to Checkout**.
4. Fill in delivery details, pick a payment method, and **Place Order**.
5. If you chose Card/UPI, you'll see a simulated payment screen with a
   spinner before being redirected to the **live tracking** page.
6. The tracking page auto-refreshes every 15 seconds to reflect any status
   changes made by the restaurant manager.

### As the restaurant manager (admin)
1. Go to `/admin/` and log in with your superuser credentials.
2. **Menu Items** — add/edit dishes, prices, and toggle `is_available` /
   `is_featured` directly from the list view (inline editing).
3. **Orders** — change the `status` dropdown (Placed → Confirmed →
   Preparing → Out for Delivery → Delivered) directly from the order list;
   this automatically writes a timestamped entry to the order's status log,
   which is what the customer sees on their tracking page.

---

## 5. Notes on "Real-Time" Tracking

This project simulates real-time tracking via **polling** (the tracking
page auto-refreshes every 15 seconds) rather than WebSockets, keeping the
stack simple (pure Django, no extra services). If you want true real-time
push updates, the natural next step is adding **Django Channels** with a
WebSocket consumer that broadcasts `OrderStatusLog` creation events — the
current `Order`/`OrderStatusLog` models are already structured to support
that without changes.

## 6. Credentials (after running `seed_menu` + `createsuperuser`)
- Create your own superuser during setup (Step 6). There are no hardcoded
  demo credentials shipped in the repo for security reasons.

## 7. Design System Reference
- **Backgrounds:** Deep Charcoal `#1a1a1a`
- **Primary accent:** Warm Orange `#ff6b35` → Tomato Red `#e8432f` gradient
- **Surfaces:** Cream/White `#fff8f0`
- All defined as CSS variables at the top of `static/css/style.css` — change
  them there to re-theme the entire site in one place.
