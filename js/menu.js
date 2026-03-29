export function initMenu() {
  const hamburger = document.querySelector('.hamburger');
  const overlay = document.querySelector('.menu-overlay');
  const sectionLinks = overlay.querySelectorAll('a[data-section]');

  function openMenu() {
    hamburger.classList.add('is-open');
    overlay.classList.add('is-open');
    document.body.classList.add('menu-open');
    hamburger.setAttribute('aria-expanded', 'true');
    overlay.setAttribute('aria-hidden', 'false');
    sectionLinks.forEach(link => link.setAttribute('tabindex', '0'));
  }

  function closeMenu() {
    hamburger.classList.remove('is-open');
    overlay.classList.remove('is-open');
    document.body.classList.remove('menu-open');
    hamburger.setAttribute('aria-expanded', 'false');
    overlay.setAttribute('aria-hidden', 'true');
    sectionLinks.forEach(link => link.setAttribute('tabindex', '-1'));
  }

  function toggleMenu() {
    if (overlay.classList.contains('is-open')) {
      closeMenu();
    } else {
      openMenu();
    }
  }

  hamburger.addEventListener('click', toggleMenu);

  sectionLinks.forEach(link => {
    link.addEventListener('click', e => {
      e.preventDefault();
      closeMenu();
      const href = link.getAttribute('href');
      document.querySelector(href).scrollIntoView({ behavior: 'smooth' });
    });
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && overlay.classList.contains('is-open')) {
      closeMenu();
    }
  });

  overlay.addEventListener('click', e => {
    if (!e.target.closest('.menu-list') && overlay.classList.contains('is-open')) {
      closeMenu();
    }
  });
}
