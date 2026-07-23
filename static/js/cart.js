/**
 * cart.js
 * Handles all cart interactions via fetch() so nothing needs a full
 * page reload: add to cart (from menu grid / detail page), and on the
 * cart page itself: increase / decrease quantity, remove item.
 *
 * Depends on: CSRF_TOKEN (set in base.html), showToast() (main.js),
 * flyToCart() (animations.js).
 */

document.addEventListener('DOMContentLoaded', function () {

  // ---------------- ADD TO CART (menu grid / item detail / carousel) ----------------
  document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
    btn.addEventListener('click', function (e) {
      const itemId = this.dataset.itemId;
      const itemImage = this.dataset.itemImage;

      // Kick off the "flying" animation immediately for instant visual feedback
      if (window.flyToCart) flyToCart(this, itemImage);

      fetch(`/cart/add/${itemId}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': CSRF_TOKEN },
      })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            document.getElementById('cart-count').innerText = data.cart_item_count;
            showToast(data.message);
          }
        })
        .catch(() => showToast('Something went wrong. Please try again.', 'danger'));
    });
  });

  // ---------------- CART PAGE: quantity +/- and remove ----------------
  document.querySelectorAll('.qty-increase, .qty-decrease').forEach(btn => {
    btn.addEventListener('click', function () {
      const itemId = this.dataset.itemId;
      const action = this.classList.contains('qty-increase') ? 'increase' : 'decrease';

      fetch(`/cart/update/${itemId}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': CSRF_TOKEN, 'Content-Type': 'application/json' },
        body: JSON.stringify({ action }),
      })
        .then(res => res.json())
        .then(() => window.location.reload()) // simplest reliable way to resync all totals/rows
        .catch(() => showToast('Could not update quantity.', 'danger'));
    });
  });

  document.querySelectorAll('.remove-item').forEach(btn => {
    btn.addEventListener('click', function () {
      const itemId = this.dataset.itemId;
      const row = this.closest('.cart-item-row');

      fetch(`/cart/remove/${itemId}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': CSRF_TOKEN },
      })
        .then(res => res.json())
        .then(() => {
          if (window.anime) {
            anime({
              targets: row,
              opacity: 0,
              height: 0,
              marginBottom: 0,
              paddingTop: 0,
              paddingBottom: 0,
              duration: 350,
              easing: 'easeInOutQuad',
              complete: () => window.location.reload(),
            });
          } else {
            window.location.reload();
          }
        });
    });
  });

});
