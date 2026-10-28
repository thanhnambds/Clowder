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



// GA4 Affiliate Link Click Tracking (event delegation)
(function() {
  const urlProductMap = {
    '4jdkN2t': 'Whisker Litter-Robot 5',
    '4e4hPtA': 'Neakasa M1 Plus',
    'neakasa': 'Neakasa M1 Plus',
    '47UgK3X': 'PETKIT Purobot Max Pro 2',
    '17052926': 'PETKIT Purobot Max Pro 2',
    '3TSWrkg': 'PETKIT Purobot Max 3',
    '17349725': 'PETKIT Purobot Max 3',
    '47KD14i': 'PETKIT Purobot Ultra',
    '17052922': 'PETKIT Purobot Ultra'
  };

  function getAffiliateProductName(link, href) {
    for (const key in urlProductMap) {
      if (href.includes(key)) return urlProductMap[key];
    }
    if (link.dataset && link.dataset.productName) {
      return link.dataset.productName;
    }
    const card = link.closest('.model-card, .leaderboard-card, .review-card, .guide-comparison-card, .hp-model, article, section');
    if (card) {
      const heading = card.querySelector('h1, h2, h3, h4, .hp-model-name');
      if (heading && heading.textContent.trim()) {
        return heading.textContent.trim();
      }
    }
    const tr = link.closest('tr');
    if (tr) {
      const prodA = tr.querySelector('a[href^="/products/"]');
      if (prodA && prodA.textContent.trim()) {
        return prodA.textContent.trim().replace(/\s*→\s*$/, '');
      }
      const th = tr.querySelector('th, td:first-child');
      if (th && th.textContent.trim()) {
        return th.textContent.trim();
      }
    }
    if (window.location.pathname.startsWith('/products/')) {
      const h1 = document.querySelector('h1');
      if (h1 && h1.textContent.trim()) {
        return h1.textContent.trim();
      }
    }
    return link.getAttribute('aria-label') || link.textContent.trim() || 'Unknown Product';
  }

  document.addEventListener('click', function(e) {
    const link = e.target.closest('a');
    if (!link) return;

    const href = link.getAttribute('href');
    if (!href || href === '#' || href.startsWith('javascript:')) return;
    if (link.classList.contains('btn-coming-soon') || (link.textContent && link.textContent.trim().toLowerCase().includes('coming soon'))) return;

    let destUrl;
    try {
      destUrl = new URL(link.href, window.location.origin);
    } catch (err) {
      return;
    }

    const rel = (link.getAttribute('rel') || '').toLowerCase();
    const isSponsored = rel.includes('sponsored');
    const isAffiliateDomain = /amzn\.to|amazon\.|anrdoezrs\.net|awin1\.com/i.test(destUrl.hostname);

    if (!isSponsored && !isAffiliateDomain) return;

    const productName = getAffiliateProductName(link, destUrl.href);

    if (typeof window.gtag === 'function') {
      window.gtag('event', 'affiliate_click', {
        product_name: productName,
        source_page: window.location.pathname,
        destination_domain: destUrl.hostname
      });
    }
  });
})();
