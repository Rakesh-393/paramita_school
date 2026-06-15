/* ═══════════════════════════════════════════════════════════════════
   PARAMITA HERITAGE SCHOOL — MAIN JS
   • Hero 3D Carousel
   • Navbar scroll effect + mobile toggle
   • 3D Card Tilt
   • Testimonial slider
   • Back to top
   • AOS init
   • Counter animation
═══════════════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  // ── AOS Init ──────────────────────────────────────────────────────
  AOS.init({
    duration: 800,
    easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
    once: true,
    offset: 60,
  });


  // ══════════════════════════════════════════════════════════════════
  // NAVBAR — scroll effect + mobile hamburger
  // ══════════════════════════════════════════════════════════════════
  const nav        = document.getElementById('siteNav');
  const hamburger  = document.getElementById('hamburger');

  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 60);
  }, { passive: true });

  hamburger?.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    nav.classList.toggle('mobile-open');
  });

  // Close mobile nav on link click
  nav?.querySelectorAll('.nav-link-item, .nav-dropdown a').forEach(link => {
    link.addEventListener('click', () => {
      hamburger?.classList.remove('open');
      nav.classList.remove('mobile-open');
    });
  });


  // ══════════════════════════════════════════════════════════════════
  // HERO 3D CAROUSEL
  // ══════════════════════════════════════════════════════════════════
  class HeroCarousel {
    constructor() {
      this.slides       = document.querySelectorAll('.hero-slide');
      this.dots         = document.querySelectorAll('.hero-dot');
      this.prevBtn      = document.getElementById('heroPrev');
      this.nextBtn      = document.getElementById('heroNext');
      this.counterEl    = document.getElementById('counterCurrent');
      this.progressFill = document.getElementById('heroProgressFill');

      this.current      = 0;
      this.total        = this.slides.length;
      this.isAnimating  = false;
      this.autoplayMs   = 6000;
      this.timer        = null;
      this.progressTimer= null;
      this.startTime    = null;

      if (this.total === 0) return;
      this.init();
    }

    init() {
      // Make sure first slide is active
      this.slides[0].classList.add('active');
      this.updateUI();
      this.startAutoplay();
      this.bindEvents();
    }

    goTo(index, direction = 'next') {
      if (this.isAnimating || index === this.current || this.total < 2) return;
      this.isAnimating = true;

      const leaving = this.slides[this.current];
      const entering = this.slides[index];

      // Exit current slide
      leaving.classList.add('exiting');

      // After a tiny frame, activate new slide
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          entering.classList.add('active');

          setTimeout(() => {
            leaving.classList.remove('active', 'exiting');
            this.current = index;
            this.updateUI();
            this.isAnimating = false;
          }, 1150);
        });
      });
    }

    next() { this.goTo((this.current + 1) % this.total, 'next'); }
    prev() { this.goTo((this.current - 1 + this.total) % this.total, 'prev'); }

    updateUI() {
      // Dots
      this.dots.forEach((d, i) => d.classList.toggle('active', i === this.current));
      // Counter
      if (this.counterEl) {
        this.counterEl.textContent = String(this.current + 1).padStart(2, '0');
      }
    }

    // ── Progress bar ──
    startProgress() {
      if (this.progressFill) {
        this.progressFill.style.transition = 'none';
        this.progressFill.style.width = '0%';
        this.startTime = performance.now();

        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            this.progressFill.style.transition = `width ${this.autoplayMs}ms linear`;
            this.progressFill.style.width = '100%';
          });
        });
      }
    }

    stopProgress() {
      if (this.progressFill) {
        this.progressFill.style.transition = 'none';
        this.progressFill.style.width = '0%';
      }
    }

    startAutoplay() {
      this.stopAutoplay();
      this.startProgress();
      this.timer = setInterval(() => {
        this.next();
        this.startProgress();
      }, this.autoplayMs);
    }

    stopAutoplay() {
      clearInterval(this.timer);
      this.stopProgress();
    }

    bindEvents() {
      this.prevBtn?.addEventListener('click', () => {
        this.stopAutoplay();
        this.prev();
        this.startAutoplay();
      });

      this.nextBtn?.addEventListener('click', () => {
        this.stopAutoplay();
        this.next();
        this.startAutoplay();
      });

      this.dots.forEach((dot, i) => {
        dot.addEventListener('click', () => {
          if (i === this.current) return;
          this.stopAutoplay();
          this.goTo(i);
          this.startAutoplay();
        });
      });

      // Keyboard
      document.addEventListener('keydown', (e) => {
        if (document.activeElement.tagName === 'INPUT') return;
        if (e.key === 'ArrowLeft')  { this.stopAutoplay(); this.prev(); this.startAutoplay(); }
        if (e.key === 'ArrowRight') { this.stopAutoplay(); this.next(); this.startAutoplay(); }
      });

      // Touch / swipe
      let touchStartX = 0;
      const hero = document.getElementById('heroSection');
      hero?.addEventListener('touchstart', e => {
        touchStartX = e.touches[0].clientX;
      }, { passive: true });
      hero?.addEventListener('touchend', e => {
        const diff = touchStartX - e.changedTouches[0].clientX;
        if (Math.abs(diff) > 50) {
          this.stopAutoplay();
          diff > 0 ? this.next() : this.prev();
          this.startAutoplay();
        }
      }, { passive: true });

      // Pause on hover
      hero?.addEventListener('mouseenter', () => this.stopAutoplay());
      hero?.addEventListener('mouseleave', () => this.startAutoplay());
    }
  }

  const heroCarousel = new HeroCarousel();


  // ══════════════════════════════════════════════════════════════════
  // 3D CARD TILT — mousemove on .tilt-card
  // ══════════════════════════════════════════════════════════════════
  const TILT_MAX   = 15;   // max degrees
  const TILT_SCALE = 1.04;

  document.querySelectorAll('.tilt-card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect   = card.getBoundingClientRect();
      const x      = e.clientX - rect.left;
      const y      = e.clientY - rect.top;
      const cx     = rect.width  / 2;
      const cy     = rect.height / 2;
      const rotX   = ((y - cy) / cy) * -TILT_MAX;
      const rotY   = ((x - cx) / cx) *  TILT_MAX;

      card.style.transform =
        `perspective(700px) rotateX(${rotX}deg) rotateY(${rotY}deg) scale(${TILT_SCALE})`;
      card.style.transition = 'transform 0.1s linear';
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(700px) rotateX(0deg) rotateY(0deg) scale(1)';
      card.style.transition = 'transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)';
    });
  });


  // ══════════════════════════════════════════════════════════════════
  // TESTIMONIAL DRAG SCROLL
  // ══════════════════════════════════════════════════════════════════
  const track   = document.getElementById('testimonialTrack');
  const tPrev   = document.getElementById('testiPrev');
  const tNext   = document.getElementById('testiNext');

  if (track) {
    // Drag scroll
    let isDown = false, startX = 0, scrollLeft = 0;

    track.addEventListener('mousedown', e => {
      isDown = true;
      track.classList.add('grabbing');
      startX    = e.pageX - track.offsetLeft;
      scrollLeft = track.scrollLeft;
    });
    track.addEventListener('mouseleave', () => { isDown = false; track.classList.remove('grabbing'); });
    track.addEventListener('mouseup',    () => { isDown = false; track.classList.remove('grabbing'); });
    track.addEventListener('mousemove', e => {
      if (!isDown) return;
      e.preventDefault();
      const x    = e.pageX - track.offsetLeft;
      const walk = (x - startX) * 2;
      track.scrollLeft = scrollLeft - walk;
    });

    // Arrow buttons
    const scrollAmount = () => track.querySelector('.testimonial-card')?.offsetWidth + 24 || 364;

    tPrev?.addEventListener('click', () => {
      track.scrollBy({ left: -scrollAmount(), behavior: 'smooth' });
    });
    tNext?.addEventListener('click', () => {
      track.scrollBy({ left: scrollAmount(), behavior: 'smooth' });
    });
  }


  // ══════════════════════════════════════════════════════════════════
  // BACK TO TOP
  // ══════════════════════════════════════════════════════════════════
  const btt = document.getElementById('backToTop');

  window.addEventListener('scroll', () => {
    btt?.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });

  btt?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });


  // ══════════════════════════════════════════════════════════════════
  // SMOOTH SCROLL for anchor links
  // ══════════════════════════════════════════════════════════════════
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const offset = document.getElementById('siteNav')?.offsetHeight || 80;
        window.scrollTo({
          top: target.getBoundingClientRect().top + window.scrollY - offset,
          behavior: 'smooth',
        });
      }
    });
  });


  // ══════════════════════════════════════════════════════════════════
  // COUNTER ANIMATION (if stat numbers exist)
  // ══════════════════════════════════════════════════════════════════
  const animateCounter = (el) => {
    const target = parseInt(el.dataset.target || el.textContent, 10);
    if (isNaN(target)) return;
    const duration = 2000;
    const step     = 16;
    const steps    = duration / step;
    let   current  = 0;
    const increment = target / steps;

    const update = () => {
      current += increment;
      el.textContent = Math.min(Math.round(current), target).toLocaleString();
      if (current < target) requestAnimationFrame(update);
    };
    requestAnimationFrame(update);
  };

  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('[data-counter]').forEach(el => counterObserver.observe(el));


  // ══════════════════════════════════════════════════════════════════
  // NAVBAR active section highlight on scroll
  // ══════════════════════════════════════════════════════════════════
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link-item');

  const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        navLinks.forEach(link => {
          link.style.color = '';
          if (link.getAttribute('href') === `#${entry.target.id}`) {
            link.style.color = 'var(--gold)';
          }
        });
      }
    });
  }, { rootMargin: '-40% 0px -55% 0px' });

  sections.forEach(s => sectionObserver.observe(s));


  // ══════════════════════════════════════════════════════════════════
  // PARALLAX — subtle on hero text (desktop only)
  // ══════════════════════════════════════════════════════════════════
  if (window.innerWidth > 900) {
    const heroContent = document.querySelector('.hero-section .slide-content');
    window.addEventListener('scroll', () => {
      const y = window.scrollY;
      if (heroContent && y < window.innerHeight) {
        heroContent.style.transform = `translateY(${y * 0.25}px)`;
        heroContent.style.opacity   = `${1 - (y / window.innerHeight) * 1.4}`;
      }
    }, { passive: true });
  }

});
