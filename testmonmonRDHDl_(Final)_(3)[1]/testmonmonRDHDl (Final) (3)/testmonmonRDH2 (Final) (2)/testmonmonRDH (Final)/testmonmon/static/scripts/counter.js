document.addEventListener('DOMContentLoaded', () => {
  initFormValidation();
  initScrollReveal();
  initLoadingButton();
  highlightNav();
  animateCounters();
});

function initFormValidation() {
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', e => {
      if (!form.checkValidity()) {
        e.preventDefault();
        e.stopPropagation();
        form.classList.add('was-validated');
      }
    });
  });
}

function initScrollReveal() {
  const animatedElements = document.querySelectorAll('.reveal');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
      }
    });
  }, { threshold: 0.1 });

  animatedElements.forEach(el => observer.observe(el));
}

function initLoadingButton() {
  const buttons = document.querySelectorAll('button[type="submit"]');
  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      const original = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Loading...';
      setTimeout(() => {
        btn.disabled = false;
        btn.innerHTML = original;
      }, 2000); // fallback reset
    });
  });
}

function highlightNav() {
  const path = window.location.pathname;
  document.querySelectorAll('.navbar .nav-link').forEach(link => {
    if (link.getAttribute('href') === path) {
      link.classList.add('active');
    }
  });
}

function animateCounters() {
  const counters = document.querySelectorAll('.counter');
  counters.forEach(counter => {
    counter.innerText = '0';
    const target = +counter.getAttribute('data-target');
    const speed = 200;
    const update = () => {
      const current = +counter.innerText;
      const increment = target / speed;
      if (current < target) {
        counter.innerText = Math.ceil(current + increment);
        setTimeout(update, 10);
      } else {
        counter.innerText = target;
      }
    };
    update();
  });
}