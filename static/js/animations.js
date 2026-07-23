/**
 * animations.js
 * Anime.js-powered micro-interactions:
 *   1. flyToCart() — a small circular clone of the food image flies from the
 *      "Add" button to the navbar cart icon, then the cart badge pulses.
 *   2. Subtle hover lift on food cards (in addition to the CSS transition,
 *      we nudge the food image slightly with anime for extra polish).
 */

/**
 * Animates a cloned circular image flying from `sourceEl` to the cart icon.
 * @param {HTMLElement} sourceEl - the button that was clicked (Add to Cart)
 * @param {string} imageUrl - the dish's image, used for the flying clone
 */
function flyToCart(sourceEl, imageUrl) {
  const cartIcon = document.querySelector('a[href*="/cart/"] .bi-cart3');
  if (!cartIcon || !window.anime) return;

  const startRect = sourceEl.getBoundingClientRect();
  const endRect = cartIcon.getBoundingClientRect();

  const flyer = document.createElement('div');
  flyer.className = 'flying-cart-item';
  flyer.style.backgroundImage = `url('${imageUrl}')`;
  flyer.style.left = `${startRect.left + startRect.width / 2 - 20}px`;
  flyer.style.top = `${startRect.top + startRect.height / 2 - 20}px`;
  document.body.appendChild(flyer);

  anime({
    targets: flyer,
    left: endRect.left + endRect.width / 2 - 20,
    top: endRect.top + endRect.height / 2 - 20,
    scale: [1, 0.2],
    opacity: [1, 0.6],
    easing: 'easeInCubic',
    duration: 700,
    complete: () => {
      flyer.remove();
      // little "pop" on the cart icon once the item "arrives"
      anime({
        targets: cartIcon,
        scale: [1, 1.35, 1],
        duration: 400,
        easing: 'easeInOutQuad',
      });
    },
  });
}

document.addEventListener('DOMContentLoaded', function () {
  if (!window.anime) return;

  // Subtle entrance animation for food cards as the page loads
  anime({
    targets: '.food-card',
    opacity: [0, 1],
    translateY: [16, 0],
    delay: anime.stagger(60),
    duration: 500,
    easing: 'easeOutQuad',
  });
});
