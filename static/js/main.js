/**
 * AUREN Fashion Store — All Client-Side Interactivity
 */

// --- NEW FEATURES FOR LUXURY EDITORIAL UPGRADE ---

function initFadeIn() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0, rootMargin: '0px 0px -50px 0px' });

  document.querySelectorAll('.fade-in, .fade-in-left, .fade-in-right').forEach(el => {
    observer.observe(el);
  });
}

function initMagneticElements() {
  document.querySelectorAll('[data-magnetic]').forEach(el => {
    const strength = parseFloat(el.dataset.magneticStrength || 3);
    const padding = parseInt(el.dataset.magneticPadding || 150);

    el.addEventListener('mousemove', (e) => {
      const rect = el.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      const distX = e.clientX - centerX;
      const distY = e.clientY - centerY;
      const inBounds =
        e.clientX > rect.left - padding &&
        e.clientX < rect.right + padding &&
        e.clientY > rect.top - padding &&
        e.clientY < rect.bottom + padding;

      if (inBounds) {
        el.style.transition = 'transform 0.3s ease-out';
        el.style.transform = `translate(${distX / strength}px, ${distY / strength}px)`;
        el.style.willChange = 'transform';
      }
    });

    el.addEventListener('mouseleave', () => {
      el.style.transition = 'transform 0.6s ease-in-out';
      el.style.transform = 'translate(0, 0)';
    });
  });
}

function initCharacterReveal() {
  document.querySelectorAll('[data-char-reveal]').forEach(el => {
    const text = el.textContent;
    el.innerHTML = '';
    text.split('').forEach((char, i) => {
      const wrapper = document.createElement('span');
      wrapper.style.cssText = 'position:relative;display:inline-block;';
      const placeholder = document.createElement('span');
      placeholder.textContent = char === ' ' ? '\u00A0' : char;
      placeholder.style.opacity = '0';
      const animated = document.createElement('span');
      animated.textContent = char === ' ' ? '\u00A0' : char;
      animated.style.cssText = `
        position:absolute;left:0;top:0;
        opacity:0.15;
        transition: opacity 0.4s ease ${i * 0.015}s;
      `;
      wrapper.appendChild(placeholder);
      wrapper.appendChild(animated);
      el.appendChild(wrapper);
    });

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const spans = el.querySelectorAll('span > span:last-child');
        if (entry.isIntersecting) {
          spans.forEach((s, i) => {
            setTimeout(() => { s.style.opacity = '1'; }, i * 18);
          });
        } else {
          spans.forEach(s => { s.style.opacity = '0.15'; });
        }
      });
    }, { threshold: 0.1 });
    observer.observe(el);
  });
}

function initCursorGlow() {
  const glow = document.getElementById('cursor-glow');
  if (!glow || window.matchMedia('(hover: none)').matches) return;
  document.addEventListener('mousemove', (e) => {
    glow.style.left = e.clientX + 'px';
    glow.style.top = e.clientY + 'px';
  });
}

function initPageTransitions() {
  const overlay = document.getElementById('page-transition');
  if (!overlay) return;

  // Fade out on load
  window.addEventListener('load', () => {
    requestAnimationFrame(() => {
      overlay.style.opacity = '0';
    });
  });

  // Fade in before navigation
  document.querySelectorAll('a[href]').forEach(link => {
    const href = link.getAttribute('href');
    
    // Skip: anchors, mailto, tel, external, blank, javascript,
    // admin URLs, and any link inside a <form>
    if (
      !href ||
      href.startsWith('#') ||
      href.startsWith('mailto') ||
      href.startsWith('tel') ||
      href.startsWith('javascript') ||
      href.startsWith('http') ||
      href.startsWith('//') ||
      link.target === '_blank' ||
      link.closest('form') !== null ||
      href.includes('/admin/')
    ) return;

    link.addEventListener('click', (e) => {
      e.preventDefault();
      overlay.style.opacity = '1';
      setTimeout(() => { window.location.href = href; }, 480);
    });
  });
}

// --- DOMContentLoaded Init Block ---

document.addEventListener('DOMContentLoaded', function () {
  // Existing core initializers
  
  // 1. Auto-dismiss alerts after 4 seconds
  const alerts = document.querySelectorAll('.custom-alert');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) {
        bsAlert.close();
      }
    }, 4000);
  });

  // 2. Sticky Navbar behavior
  const mainNav = document.getElementById('mainNav');
  if (mainNav) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 20) {
        mainNav.style.padding = '0.6rem 0';
        mainNav.style.backgroundColor = 'rgba(250, 250, 248, 0.98)';
        mainNav.style.boxShadow = '0 5px 20px rgba(0,0,0,0.03)';
      } else {
        mainNav.style.padding = '1rem 0';
        mainNav.style.backgroundColor = 'rgba(250, 250, 248, 0.95)';
        mainNav.style.boxShadow = 'none';
      }
    });
  }

  // 3. Product Gallery (Detail Page)
  const mainGalleryImg = document.getElementById('mainGalleryImg');
  const thumbs = document.querySelectorAll('.detail-thumb');
  thumbs.forEach(function (thumb) {
    thumb.addEventListener('click', function () {
      // Set active thumbnail
      thumbs.forEach(t => t.classList.remove('active'));
      thumb.classList.add('active');
      
      // Swap main image src
      const newSrc = thumb.dataset.large;
      if (mainGalleryImg && newSrc) {
        mainGalleryImg.style.opacity = 0;
        setTimeout(() => {
          mainGalleryImg.src = newSrc;
          mainGalleryImg.style.opacity = 1;
        }, 150);
      }
    });
  });

  // 4. Quantity Selector (Detail Page)
  const qtyInput = document.getElementById('qtyInput');
  const qtyFormInput = document.getElementById('qtyFormInput');
  const btnMinus = document.getElementById('qtyMinus');
  const btnPlus = document.getElementById('qtyPlus');

  if (qtyInput) {
    if (btnMinus) {
      btnMinus.addEventListener('click', function () {
        let current = parseInt(qtyInput.value) || 1;
        if (current > 1) {
          qtyInput.value = current - 1;
          if (qtyFormInput) qtyFormInput.value = qtyInput.value;
        }
      });
    }
    if (btnPlus) {
      btnPlus.addEventListener('click', function () {
        let current = parseInt(qtyInput.value) || 1;
        const max = parseInt(qtyInput.getAttribute('max')) || 99;
        if (current < max) {
          qtyInput.value = current + 1;
          if (qtyFormInput) qtyFormInput.value = qtyInput.value;
        }
      });
    }
    qtyInput.addEventListener('change', function () {
      let current = parseInt(qtyInput.value) || 1;
      const max = parseInt(qtyInput.getAttribute('max')) || 99;
      if (current < 1) current = 1;
      if (current > max) current = max;
      qtyInput.value = current;
      if (qtyFormInput) qtyFormInput.value = current;
    });
  }

  // Initializing new luxury design components
  initFadeIn();
  initMagneticElements();
  initCharacterReveal();
  initCursorGlow();
  initPageTransitions();
});

// --- GLOBAL UTILITY FUNCTIONS ---

// 5. Size selector buttons (Detail Page)
function selectDetailSize(button, size) {
  // Reset all size buttons in selector
  const buttons = document.querySelectorAll('.detail-size-btn');
  buttons.forEach(btn => btn.classList.remove('active'));
  
  // Activate selected button
  button.classList.add('active');
  
  // Set hidden input value in the form
  const sizeInput = document.getElementById('sizeInput');
  if (sizeInput) {
    sizeInput.value = size;
  }
}

// 6. Size filter buttons toggle (Shop Page)
function toggleSizeFilter(button, size) {
  const hiddenInput = document.getElementById('sizeHidden' + size);
  if (hiddenInput) {
    if (hiddenInput.checked) {
      hiddenInput.checked = false;
      button.classList.remove('active');
    } else {
      hiddenInput.checked = true;
      button.classList.add('active');
    }
  }
}

// 7. Sort selection handler (Shop Page)
function handleSort(value) {
  const sortInput = document.getElementById('sortInput');
  const filterForm = document.getElementById('filterForm');
  if (sortInput && filterForm) {
    sortInput.value = value;
    filterForm.submit();
  }
}

// 8. Newsletter Submission
function handleNewsletterSubmit(event) {
  event.preventDefault();
  const emailInput = document.getElementById('newsletterEmail');
  if (emailInput) {
    const email = emailInput.value;
    // Show premium visual feedback
    const container = document.getElementById('messagesContainer') || document.body;
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show custom-alert';
    alertDiv.setAttribute('role', 'alert');
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '90px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '1050';
    alertDiv.innerHTML = `
      <i class="fa-solid fa-circle-check me-2"></i>
      Thank you! ${email} has been subscribed to AUREN Fashion updates.
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);
    emailInput.value = '';
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alertDiv);
      if (bsAlert) bsAlert.close();
    }, 4000);
  }
}
