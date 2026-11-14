/* A2T Distributions — Main JS */

// NAV SCROLL
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 40);
});

// MOBILE BURGER
const burger = document.getElementById('burger');
const navLinks = document.getElementById('navLinks');
if (burger) {
  burger.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    burger.classList.toggle('active');
  });
}

// REVEAL ON SCROLL
const revealEls = document.querySelectorAll('.reveal');
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => {
        entry.target.classList.add('visible');
      }, i * 80);
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

revealEls.forEach(el => revealObserver.observe(el));

// COUNTER ANIMATION
function animateCounter(el, target, duration = 1600) {
  let start = 0;
  const step = (timestamp) => {
    if (!start) start = timestamp;
    const progress = Math.min((timestamp - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.floor(eased * target);
    if (progress < 1) requestAnimationFrame(step);
    else el.textContent = target;
  };
  requestAnimationFrame(step);
}

const counters = document.querySelectorAll('.stat__num[data-target]');
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      animateCounter(entry.target, parseInt(entry.target.dataset.target));
      counterObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

counters.forEach(c => counterObserver.observe(c));

// ACTIVE NAV LINK
const norm = p => (p || '').replace(/^(\.\.\/)+/, '').replace(/^\//, '').replace(/(^|\/)index\.html$/, '$1').replace(/\.html$/, '').replace(/\/$/, '');
const currentPage = norm(window.location.pathname);
document.querySelectorAll('.nav__link').forEach(link => {
  const href = norm(link.getAttribute('href'));
  link.classList.toggle('active', href === currentPage || (href === 'blog' && currentPage.startsWith('blog')));
});

// LYA (assistante du .com) : chargée 1,5 s après l'affichage, pour ne pas ralentir la page
(function () {
  const src = ((document.currentScript && document.currentScript.src) || '').replace(/main\.js(\?.*)?$/, 'lya.js');
  if (!src) return;
  const go = () => { const s = document.createElement('script'); s.src = src; s.defer = true; document.body.appendChild(s); };
  if (document.readyState === 'complete') setTimeout(go, 1500);
  else window.addEventListener('load', () => setTimeout(go, 1500));
})();

/* 14/11/2026 : compteur de vues du blog (functions/api/vues.js).
   Article : compte la lecture (1 fois / 12 h par visiteur) et affiche « 👁 N vues » dans la ligne d'infos.
   Index du blog : affiche les vues sur chaque carte. Rien n'est affiché sous SEUIL vues. */
(function () {
  var SEUIL = 20;
  var chemin = location.pathname.replace(/\.html$/, '').replace(/\/$/, '');
  if (chemin.indexOf('/blog') !== 0) return;
  function txt(n) { return '👁 ' + n.toLocaleString('fr-FR') + ' vues'; }
  var slug = chemin.split('/')[2];
  if (slug && slug !== 'index') {
    var cle = 'vu:' + slug, deja = false;
    try { deja = Date.now() - (+localStorage.getItem(cle) || 0) < 12 * 3600 * 1000; } catch (e) {}
    fetch('/api/vues?p=' + slug, { method: deja ? 'GET' : 'POST' })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        try { if (!deja) localStorage.setItem(cle, String(Date.now())); } catch (e) {}
        var n = d[slug], meta = document.querySelector('.article-meta');
        if (meta && n >= SEUIL) { var s = document.createElement('span'); s.textContent = txt(n); meta.appendChild(s); }
      }).catch(function () {});
    return;
  }
  var cartes = {}, liens = document.querySelectorAll('.blog-card h2 a[href^="/blog/"]');
  for (var i = 0; i < liens.length; i++) cartes[liens[i].getAttribute('href').split('/')[2]] = liens[i];
  var slugs = Object.keys(cartes);
  if (!slugs.length) return;
  fetch('/api/vues?p=' + slugs.join(',')).then(function (r) { return r.json(); }).then(function (d) {
    slugs.forEach(function (s) {
      var pied = cartes[s].closest('.blog-card').querySelector('.blog-card__footer span:last-child');
      if (pied && d[s] >= SEUIL) pied.textContent += ' · ' + txt(d[s]);
    });
  }).catch(function () {});
})();
