document.documentElement.classList.add('js-loaded');

document.addEventListener('DOMContentLoaded', () => {
  const menuBtn = document.getElementById('mobile-menu-btn');
  const navMenu = document.getElementById('nav-menu');
  if (menuBtn && navMenu) {
    menuBtn.addEventListener('click', () => {
      const open = navMenu.classList.toggle('open');
      menuBtn.classList.toggle('active', open);
      menuBtn.setAttribute('aria-expanded', String(open));
    });
    navMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
        menuBtn.classList.remove('active');
        menuBtn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  const dropdowns = document.querySelectorAll('.nav-item-dropdown');
  dropdowns.forEach(drop => {
    const btn = drop.querySelector('.nav-dropdown-toggle');
    if (!btn) return;

    let hoverTimer;

    drop.addEventListener('mouseenter', () => {
      if (window.innerWidth > 768) {
        clearTimeout(hoverTimer);
        dropdowns.forEach(d => {
          if (d !== drop) {
            d.classList.remove('open');
            d.querySelector('.nav-dropdown-toggle')?.setAttribute('aria-expanded', 'false');
          }
        });
        drop.classList.add('open');
        btn.setAttribute('aria-expanded', 'true');
      }
    });

    drop.addEventListener('mouseleave', () => {
      if (window.innerWidth > 768) {
        hoverTimer = setTimeout(() => {
          drop.classList.remove('open');
          btn.setAttribute('aria-expanded', 'false');
        }, 150);
      }
    });

    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = drop.classList.contains('open');
      dropdowns.forEach(d => {
        d.classList.remove('open');
        d.querySelector('.nav-dropdown-toggle')?.setAttribute('aria-expanded', 'false');
      });
      if (!isOpen) {
        drop.classList.add('open');
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-item-dropdown')) {
      dropdowns.forEach(d => {
        d.classList.remove('open');
        d.querySelector('.nav-dropdown-toggle')?.setAttribute('aria-expanded', 'false');
      });
    }
    if (navMenu && menuBtn && !navMenu.contains(e.target) && !menuBtn.contains(e.target) && navMenu.classList.contains('open')) {
      navMenu.classList.remove('open');
      menuBtn.classList.remove('active');
      menuBtn.setAttribute('aria-expanded', 'false');
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      dropdowns.forEach(d => {
        const b = d.querySelector('.nav-dropdown-toggle');
        const hadFocus = d.contains(document.activeElement);
        d.classList.remove('open');
        if (b) {
          b.setAttribute('aria-expanded', 'false');
          if (hadFocus) b.focus();
        }
      });
      if (navMenu && navMenu.classList.contains('open')) {
        navMenu.classList.remove('open');
        menuBtn?.classList.remove('active');
        menuBtn?.setAttribute('aria-expanded', 'false');
        menuBtn?.focus();
      }
    }
  });

  // Mobile tables: swipe hint & right edge fade (D)
  const tableWrappers = document.querySelectorAll('.table-responsive');
  tableWrappers.forEach(wrapper => {
    let hint = wrapper.previousElementSibling;
    const isExistingHint = hint && (hint.classList.contains('swipe-hint') || hint.classList.contains('table-swipe-hint'));
    if (!isExistingHint) {
      hint = document.createElement('div');
      hint.className = 'table-swipe-hint';
      hint.innerHTML = '<span>Swipe to compare &rarr;</span>';
      wrapper.parentNode.insertBefore(hint, wrapper);
    } else {
      hint.innerHTML = '<span>Swipe to compare &rarr;</span>';
    }

    let hasScrolled = false;

    function updateTableHints() {
      const isMobile = window.innerWidth <= 640;
      const isOverflowing = wrapper.scrollWidth > wrapper.clientWidth + 2;
      const canScrollRight = wrapper.scrollLeft < (wrapper.scrollWidth - wrapper.clientWidth - 4);

      if (isMobile && isOverflowing && !hasScrolled) {
        hint.style.display = 'inline-flex';
      } else {
        hint.style.display = 'none';
      }

      if (isOverflowing && canScrollRight) {
        wrapper.classList.add('has-fade-right');
      } else {
        wrapper.classList.remove('has-fade-right');
      }
    }

    wrapper.addEventListener('scroll', () => {
      if (wrapper.scrollLeft > 10) {
        hasScrolled = true;
        hint.style.display = 'none';
      }
      const canScrollRight = wrapper.scrollLeft < (wrapper.scrollWidth - wrapper.clientWidth - 4);
      if (canScrollRight) {
        wrapper.classList.add('has-fade-right');
      } else {
        wrapper.classList.remove('has-fade-right');
      }
    }, { passive: true });

    updateTableHints();
    window.addEventListener('resize', updateTableHints);
  });
});

