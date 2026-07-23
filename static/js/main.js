/**
 * main.js
 * General small UI helpers shared across pages.
 */

document.addEventListener('DOMContentLoaded', function () {
  // Highlight the current page's nav link
  const currentPath = window.location.pathname;
  document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // Auto-dismiss Bootstrap alerts after 4 seconds
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      const instance = bootstrap.Alert.getOrCreateInstance(alert);
      instance.close();
    }, 4000);
  });
});

/** Small toast helper reused by cart.js for "Added to cart" feedback */
function showToast(message, type = 'success') {
  const toastEl = document.createElement('div');
  toastEl.className = `position-fixed top-0 end-0 m-3 alert alert-${type} shadow`;
  toastEl.style.zIndex = 3000;
  toastEl.innerText = message;
  document.body.appendChild(toastEl);
  setTimeout(() => toastEl.remove(), 2200);
}
