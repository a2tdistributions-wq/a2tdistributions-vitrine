/* A2T Distributions — Lya, l'assistante du .com, sur le site vitrine.
   Chargée par main.js après l'affichage de la page. Les réponses viennent du même moteur que
   la bulle de a2tdistributions.com (point d'accès lya-fr.php, réservé au .fr). Les liens vers
   le .com reçoivent les UTM du .fr (règle : le .fr renvoie vers le .com, sans contenu dupliqué). */
(function () {
  if (window.__a2tLya) return;
  window.__a2tLya = true;

  var API = 'https://a2tdistributions.com/lya-fr.php';
  var PHONE = '02 97 32 76 11';
  var WELCOME = 'Bonjour, je suis Lya. Je vous aide à trouver le bon produit, à comprendre une cote ou à suivre une commande. Que cherchez-vous ?';
  var KEY = 'a2t-lya-fr';
  // aussi chargée par ouverture-france.fr (script dans le bloc « Nos partenaires » de FD Manager)
  var SITE = location.hostname.replace(/^www\./, '');
  var CONTACT = /ouverture-france/.test(SITE) ? '/contactez-votre-expert-menuiserie-cleguer.html' : '/contact';
  var pageSlug = (location.pathname.replace(/^\/|\/$/g, '').replace(/\.html$/, '').replace(/\//g, '-')) || 'accueil';

  var css = ''
    + '.lya{--lya-red:#c10f17;--lya-dark:#1d2227;--lya-bg:#fff;--lya-soft:#f3f1ee;--lya-text:#1d2227;--lya-mute:#5d6166;'
    + 'position:fixed;right:16px;bottom:calc(16px + var(--lya-lift,0px));z-index:10050;font-family:inherit;font-size:15px;line-height:1.45;color:var(--lya-text)}'
    + '.lya *{box-sizing:border-box}'
    + '.lya div,.lya span,.lya strong,.lya small,.lya a,.lya button,.lya input,.lya form,.lya label{margin:0;text-transform:none;letter-spacing:normal;'
    + 'text-shadow:none;float:none;min-height:0;max-height:none;line-height:1.45}'
    + '.lya button,.lya input{font-family:inherit;width:auto;height:auto;box-shadow:none}'
    + '.lya .lya__panel,.lya .lya__head{padding-top:0;margin-top:0}'
    + '.lya__btn{display:flex;align-items:center;gap:8px;border:0;border-radius:999px;background:var(--lya-red);color:#fff;'
    + 'padding:8px 16px 8px 8px;font:inherit;font-weight:600;cursor:pointer;box-shadow:0 6px 18px rgba(193,15,23,.32)}'
    + '.lya__btn:focus-visible,.lya__send:focus-visible,.lya__close:focus-visible{outline:3px solid #ffd27a;outline-offset:2px}'
    + '.lya__ico{width:32px;height:32px;border-radius:50%;background:rgba(255,255,255,.18);display:grid;place-items:center}'
    + '.lya__ico svg{width:18px;height:18px}'
    + '.lya__panel{position:absolute;right:0;bottom:0;width:370px;max-width:calc(100vw - 32px);height:540px;max-height:calc(100vh - 32px);'
    + 'background:var(--lya-bg);border-radius:14px;box-shadow:0 18px 50px rgba(0,0,0,.28);display:flex;flex-direction:column;overflow:hidden}'
    + '.lya__panel[hidden]{display:none}'
    + '.lya__head{background:var(--lya-dark);color:#fff;padding:12px 14px;display:flex;align-items:center;gap:10px}'
    + '.lya__head .lya__ico{background:var(--lya-red)}'
    + '.lya__head strong{display:block;font-size:15px}.lya__head small{display:block;opacity:.75;font-size:12px}'
    + '.lya__close{margin-left:auto;border:0;background:transparent;color:#fff;font-size:26px;line-height:1;cursor:pointer;padding:0 4px}'
    + '.lya__msgs{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px;background:var(--lya-soft)}'
    + '.lya__msgs>*{flex-shrink:0}'
    + '.lya__m{max-width:88%;padding:9px 12px;border-radius:12px;white-space:pre-wrap;overflow-wrap:anywhere}'
    + '.lya__m--bot{background:#fff;border:1px solid #e4e0da;align-self:flex-start;border-bottom-left-radius:4px}'
    + '.lya__m--me{background:var(--lya-red);color:#fff;align-self:flex-end;border-bottom-right-radius:4px}'
    + '.lya .lya__m a{color:var(--lya-red)!important;font-weight:600;text-decoration:underline}'
    + '.lya__m--wait{color:var(--lya-mute);font-style:italic}'
    + '.lya__sugg{display:flex;flex-direction:column;gap:6px;align-self:stretch}'
    + '.lya__card{display:block;background:#fff;border:1px solid #e4e0da;border-left:3px solid var(--lya-red);border-radius:8px;'
    + 'padding:8px 10px;color:var(--lya-text);text-decoration:none;font-size:14px}'
    + '.lya__card span{display:block;color:var(--lya-red);font-weight:600;font-size:13px;margin-top:2px}'
    + '.lya__form{display:flex;gap:8px;padding:10px;border-top:1px solid #e4e0da;background:#fff}'
    + '.lya__in{flex:1;min-width:0;border:1px solid #cfcac3;border-radius:10px;padding:10px 12px;font:inherit;font-size:16px;color:var(--lya-text)}'
    + '.lya .lya__send{border:0;border-radius:10px;background:var(--lya-red)!important;color:#fff!important;font:inherit;font-weight:600;padding:0 14px;cursor:pointer}'
    + '.lya__send:disabled{opacity:.5;cursor:default}'
    + '.lya__foot{padding:6px 12px 10px;background:#fff;font-size:12px;color:var(--lya-mute);text-align:center}'
    + '.lya__foot a{color:var(--lya-mute)}'
    + '@media (max-width:640px){.lya{right:12px;bottom:calc(12px + var(--lya-lift,0px))}.lya__btn{padding:10px;width:52px;height:52px;justify-content:center}'
    + '.lya__btn .lya__lbl{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}.lya__btn .lya__ico{background:none}'
    + '.lya--open .lya__btn{display:none}.lya__panel{position:fixed;right:8px;left:8px;bottom:8px;width:auto;max-width:none;bottom:calc(8px + var(--lya-lift,0px));height:min(560px,calc(100vh - 16px - var(--lya-lift,0px)))}}'
    + '@media print{.lya{display:none}}';

  var bubble = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    + '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg>';

  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  var root = document.createElement('div');
  root.className = 'lya';
  root.innerHTML = ''
    + '<button class="lya__btn" type="button" aria-expanded="false" aria-controls="lya-panel">'
    + '<span class="lya__ico">' + bubble + '</span><span class="lya__lbl">Une question ? Lya</span></button>'
    + '<div class="lya__panel" id="lya-panel" role="dialog" aria-label="Lya, assistante A2T Distributions" hidden>'
    + '<div class="lya__head"><span class="lya__ico">' + bubble + '</span>'
    + '<div><strong>Lya, assistante A2T Distributions</strong><small>Réponse immédiate, 7 j/7</small></div>'
    + '<button class="lya__close" type="button" aria-label="Fermer">×</button></div>'
    + '<div class="lya__msgs" aria-live="polite"></div>'
    + '<form class="lya__form"><label class="lya__lbl" for="lya-in" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Votre question</label>'
    + '<input class="lya__in" id="lya-in" type="text" maxlength="500" autocomplete="off" placeholder="Votre question…">'
    + '<button class="lya__send" type="submit">Envoyer</button></form>'
    + '<div class="lya__foot">Un humain ? <a href="tel:+33297327611">' + PHONE + '</a> · <a href="' + CONTACT + '">Nous écrire</a></div>'
    + '</div>';
  document.body.appendChild(root);

  function lift() {
    var bar = document.getElementById('contactButtonsMobile');
    var h = 0;
    if (bar && bar.offsetHeight && getComputedStyle(bar).position === 'fixed') {
      var r = bar.getBoundingClientRect();
      if (r.top > window.innerHeight / 2 && r.top < window.innerHeight) h = Math.round(window.innerHeight - r.top);
    }
    root.style.setProperty('--lya-lift', h + 'px');
  }
  lift();
  window.addEventListener('resize', lift);
  window.addEventListener('scroll', lift, { passive: true });

  var btn = root.querySelector('.lya__btn');
  var panel = root.querySelector('.lya__panel');
  var msgs = root.querySelector('.lya__msgs');
  var form = root.querySelector('.lya__form');
  var input = root.querySelector('.lya__in');
  var send = root.querySelector('.lya__send');
  var history = [];

  function load() {
    try { history = JSON.parse(sessionStorage.getItem(KEY) || '[]') || []; } catch (e) { history = []; }
  }
  function save() {
    try { sessionStorage.setItem(KEY, JSON.stringify(history.slice(-30))); } catch (e) { /* stockage indisponible */ }
  }

  // pas de new URL() : ouverture-france.fr écrase window.URL avec une chaîne
  function parts(url) {
    var m = /^https?:\/\/([^\/?#]+)([^?#]*)(\?[^#]*)?/i.exec(String(url || ''));
    return m ? { host: m[1].toLowerCase(), path: m[2] || '/', search: m[3] || '' } : null;
  }

  function withUtm(url) {
    var u = parts(url);
    if (!u || !/(^|\.)a2tdistributions\.com$/.test(u.host)) return null;
    // ajout à la main : « ?drutex » doit rester « ?drutex » (lu par les configurateurs)
    var utm = 'utm_source=' + encodeURIComponent(/a2tdistributions-vitrine|^localhost/.test(SITE) ? 'a2tdistributions.fr' : SITE) + '&utm_medium=lya&utm_campaign=chat-' + encodeURIComponent(pageSlug);
    var base = String(url).split('#')[0];
    return base + (base.indexOf('?') === -1 ? '?' : '&') + utm;
  }

  function shortLabel(url) {
    var u = parts(url);
    if (!u) return url;
    var path = u.path.replace(/\/$/, '');
    try { path = decodeURIComponent(path); } catch (e) { /* chemin laissé tel quel */ }
    var label = u.host.replace(/^www\./, '') + path + (u.search && /configurateur/.test(path) ? u.search : '');
    return label.length > 48 ? label.slice(0, 46) + '…' : label;
  }

  function fillText(node, text) {
    var parts = String(text || '').split(/(https?:\/\/[^\s]+)/g);
    parts.forEach(function (part) {
      if (!part) return;
      if (/^https?:\/\//.test(part)) {
        var href = withUtm(part);
        if (href) {
          var a = document.createElement('a');
          a.href = href;
          a.target = '_blank';
          a.rel = 'noopener';
          a.textContent = shortLabel(part);
          node.appendChild(a);
          return;
        }
      }
      node.appendChild(document.createTextNode(part));
    });
  }

  function addMsg(role, text, suggestions) {
    var m = document.createElement('div');
    m.className = 'lya__m lya__m--' + (role === 'me' ? 'me' : 'bot');
    if (role === 'me') m.textContent = text; else fillText(m, text);
    msgs.appendChild(m);
    if (suggestions && suggestions.length) {
      var box = document.createElement('div');
      box.className = 'lya__sugg';
      suggestions.slice(0, 3).forEach(function (s) {
        var href = withUtm(s.url);
        if (!href) return;
        var a = document.createElement('a');
        a.className = 'lya__card';
        a.href = href;
        a.target = '_blank';
        a.rel = 'noopener';
        a.textContent = s.title;
        var go = document.createElement('span');
        go.textContent = (s.label || 'Voir le produit') + ' →';
        a.appendChild(go);
        box.appendChild(a);
      });
      if (box.childNodes.length) msgs.appendChild(box);
    }
    msgs.scrollTop = msgs.scrollHeight;
    return m;
  }

  function render() {
    msgs.textContent = '';
    addMsg('bot', WELCOME);
    history.forEach(function (h) { addMsg(h.r, h.t, h.s); });
  }

  function open(state) {
    panel.hidden = !state;
    root.classList.toggle('lya--open', state);
    btn.setAttribute('aria-expanded', state ? 'true' : 'false');
    if (state) {
      if (!msgs.childNodes.length) render();
      setTimeout(function () { input.focus(); }, 50);
    } else {
      btn.focus();
    }
  }

  btn.addEventListener('click', function () { open(true); });
  root.querySelector('.lya__close').addEventListener('click', function () { open(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) open(false); });

  // A2T 01/11/2026 (Thierry) : au bout de 15 s sur une page, petite bulle d'invitation à côté du bouton de Lya,
  // une seule fois par visite ; jamais si la fenêtre est déjà ouverte ; disparaît seule (8 s sur smartphone, 20 s sinon)
  function a2tInviteLya(btnEl, estOuvert, ouvrir) {
    var CLE = 'a2t-lya-invite';
    try { if (sessionStorage.getItem(CLE)) return; } catch (e) { return; }
    if (/^(checkout|cart|order-confirmation|authentication|password)$/.test(document.body.id || '')) return;
    var t = 0;
    var iv = setInterval(function () {
      if (document.hidden) return;
      if (estOuvert()) { clearInterval(iv); return; }
      t += 1000;
      if (t < 15000) return;
      clearInterval(iv);
      try { sessionStorage.setItem(CLE, '1'); } catch (e) {}
      var r = btnEl.getBoundingClientRect();
      if (!r.width) return;
      var b = document.createElement('div');
      b.setAttribute('role', 'status');
      b.style.cssText = 'position:fixed;z-index:10060;max-width:min(270px,calc(100vw - 32px));right:' + Math.max(8, Math.round(window.innerWidth - r.right)) + 'px;bottom:' + Math.round(window.innerHeight - r.top + 10) + 'px;display:flex;align-items:flex-start;gap:6px;background:#fff;color:#1d2227;border:1px solid #e0dcd5;border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.18);padding:10px 8px 10px 12px;font:14px/1.4 inherit;font-family:inherit';
      b.innerHTML = '<button type="button" style="all:unset;cursor:pointer;flex:1"><strong style="display:block;color:#c10f17">Bonjour, je suis Lya</strong>Je vous aide à trouver le bon produit ou le prix ?</button>'
        + '<button type="button" aria-label="Fermer" style="all:unset;cursor:pointer;color:#80858a;font-size:20px;line-height:1;padding:0 4px">×</button>';
      document.body.appendChild(b);
      var fin = function () { if (b.parentNode) b.parentNode.removeChild(b); };
      b.firstChild.addEventListener('click', function () { fin(); ouvrir(); });
      b.lastChild.addEventListener('click', fin);
      btnEl.addEventListener('click', fin);
      setTimeout(fin, window.matchMedia('(max-width:640px)').matches ? 8000 : 20000);
    }, 1000);
  }
  a2tInviteLya(btn, function () { return !panel.hidden; }, function () { open(true); });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var q = input.value.trim();
    if (!q || send.disabled) return;
    input.value = '';
    addMsg('me', q);
    history.push({ r: 'me', t: q });
    save();
    send.disabled = true;
    var wait = addMsg('bot', 'Lya écrit…');
    wait.classList.add('lya__m--wait');
    fetch(API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: q,
        page_title: document.title,
        device_type: window.matchMedia('(max-width: 640px)').matches ? 'mobile' : 'desktop',
        user_lang: navigator.language || 'fr'
      })
    }).then(function (r) { return r.json(); }).then(function (j) {
      wait.remove();
      var t = (j && j.answer) || 'Désolée, je n’ai pas pu répondre. Appelez-nous au ' + PHONE + '.';
      var s = (j && j.suggestions) || [];
      addMsg('bot', t, s);
      history.push({ r: 'bot', t: t, s: s });
      save();
    }).catch(function () {
      wait.remove();
      addMsg('bot', 'La connexion a échoué. Réessayez, ou appelez-nous au ' + PHONE + '.');
    }).then(function () {
      send.disabled = false;
      input.focus();
    });
  });

  load();
})();
