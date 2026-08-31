document.addEventListener('DOMContentLoaded', () => {
  const header = document.getElementById('header');
  const hamburger = document.getElementById('hamburger');
  const nav = document.getElementById('nav');
  const backToTop = document.getElementById('backToTop');
  const yearEl = document.getElementById('year');
  const form = document.getElementById('contactForm');
  const formNote = document.getElementById('formNote');

  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Mobile nav toggle
  if (hamburger && nav) {
    hamburger.addEventListener('click', () => {
      const isOpen = nav.classList.toggle('active');
      hamburger.classList.toggle('active', isOpen);
      hamburger.setAttribute('aria-expanded', String(isOpen));
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    nav.querySelectorAll('.nav__link, .nav__cta').forEach(link => {
      link.addEventListener('click', () => {
        nav.classList.remove('active');
        hamburger.classList.remove('active');
        hamburger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });
  }

  // Header + back-to-top on scroll
  const onScroll = () => {
    const scrolled = window.scrollY > 20;
    header.classList.toggle('scrolled', scrolled);
    backToTop.classList.toggle('show', window.scrollY > 500);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Reveal-on-scroll animation
  const revealEls = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(el => observer.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('in-view'));
  }

  // Contact form (client-side demo submit)
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      formNote.textContent = "Thanks! Your message has been sent — I'll be in touch within 24 hours.";
      form.reset();
    });
  }
});
