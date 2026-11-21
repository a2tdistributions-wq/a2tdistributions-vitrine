/* Appli A2T (21/11/2026) : sur le .fr, le bandeau renvoie vers l'appli A2T du .com (une seule appli pour les deux sites).
   Sur ordinateur : QR code pour l'installer sur le téléphone. Bandeau par-dessus la page (rien ne bouge), fermé = 14 jours. */
(function () {
  var d = document, CLE = 'a2t_appli_non', COM = 'https://a2tdistributions.com';
  var LIEN = COM + '/?installer=1&utm_source=a2t_fr&utm_medium=appli';
  var refuse = 0; try { refuse = +localStorage.getItem(CLE) || 0; } catch (e) {}
  if (Date.now() - refuse < 14 * 864e5) return;
  var pc = matchMedia('(hover:hover) and (pointer:fine)').matches && innerWidth >= 900;
  var css = '.a2t-appli{position:fixed;left:0;right:0;top:0;z-index:2147483000;background:#1e2326;color:#eef0ee;box-shadow:0 4px 18px rgba(0,0,0,.35);font:14px/1.3 "Hanken Grotesk",system-ui,sans-serif;transform:translateY(-110%);transition:transform .35s ease}'
    + '.a2t-appli.vu{transform:none}.a2t-appli .in{max-width:1248px;margin:0 auto;display:flex;align-items:center;gap:12px;padding:9px 14px}'
    + '.a2t-appli img{width:38px;height:38px;border-radius:9px;flex:none}.a2t-appli .t{flex:1;min-width:0}.a2t-appli .t b{display:block;font-size:15px}.a2t-appli .t span{color:#b9c1c4;font-size:12.5px}'
    + '.a2t-appli a,.a2t-appli button{font:inherit;cursor:pointer;border-radius:999px;border:0;padding:9px 16px;font-weight:700;white-space:nowrap;text-decoration:none}.a2t-appli .ok{background:#d3263a;color:#fff}'
    + '.a2t-appli .x{background:none;color:#b9c1c4;font-size:22px;line-height:1;padding:6px 8px}'
    + '.a2t-appli-fond{position:fixed;inset:0;z-index:2147483001;background:rgba(0,0,0,.55);display:grid;place-items:center;padding:16px}'
    + '.a2t-appli-boite{background:#fff;color:#1e2326;border-radius:16px;max-width:360px;width:100%;padding:22px;text-align:center;font:15px/1.45 "Hanken Grotesk",system-ui,sans-serif}'
    + '.a2t-appli-boite h3{margin:0 0 8px;font-size:19px}.a2t-appli-boite img{display:block;margin:8px auto 0;width:220px;height:220px;max-width:100%;image-rendering:pixelated}'
    + '.a2t-appli-boite button{display:block;margin:14px auto 0;background:#1e2326;color:#fff;border:0;border-radius:10px;padding:11px 20px;font:inherit;font-weight:700;cursor:pointer}'
    + '@media (max-width:560px){.a2t-appli .t span{display:none}.a2t-appli .in{padding:8px 10px;gap:9px}}';
  function montrer() {
    var st = d.createElement('style'); st.textContent = css; d.head.appendChild(st);
    var b = d.createElement('div'); b.className = 'a2t-appli'; b.setAttribute('role', 'region'); b.setAttribute('aria-label', "Installer l'appli A2T");
    b.innerHTML = '<div class="in"><img src="' + COM + '/appli/a2t-192.png" alt="" width="38" height="38"><div class="t"><b>L\'appli A2T</b><span>Configurez, chiffrez et commandez en un clic, depuis votre écran d\'accueil.</span></div>'
      + (pc ? '<button type="button" class="ok" data-a="qr">Installer sur mon téléphone</button>' : '<a class="ok" href="' + LIEN + '">Installer</a>')
      + '<button type="button" class="x" data-a="non" aria-label="Fermer">×</button></div>';
    b.onclick = function (e) {
      var a = e.target.closest && e.target.closest('[data-a]'); if (!a) return;
      if (a.getAttribute('data-a') === 'non') { try { localStorage.setItem(CLE, String(Date.now())); } catch (x) {} b.classList.remove('vu'); setTimeout(function () { b.remove(); }, 400); }
      else {
        var f = d.createElement('div'); f.className = 'a2t-appli-fond';
        f.innerHTML = '<div class="a2t-appli-boite" role="dialog" aria-modal="true"><h3>Installer l\'appli sur votre téléphone</h3><p>Scannez ce code avec l\'appareil photo du téléphone, puis touchez « Installer ».</p><img src="' + COM + '/appli/qr-installer.png" alt="QR code pour installer l\'appli A2T" width="220" height="220"><button type="button">Fermer</button></div>';
        f.onclick = function (ev) { if (ev.target === f || ev.target.tagName === 'BUTTON') f.remove(); };
        d.body.appendChild(f);
      }
    };
    d.body.appendChild(b);
    requestAnimationFrame(function () { requestAnimationFrame(function () { b.classList.add('vu'); }); });
  }
  setTimeout(montrer, 3500);
})();
