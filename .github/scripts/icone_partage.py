"""18/10/2026 (remarque de Thierry : le .fr affiche un globe bleu au lieu de l'icône A2T, et ses pages n'ont pas d'image de partage) :
ajoute à chaque page HTML l'icône A2T (même que le .com) et, si absente, une image de partage og:image / twitter:image
= la première vraie photo de la page (assets/images, assets/media), sinon la façade du showroom.
Relançable sans risque : ne rajoute rien si c'est déjà présent. Usage (racine du dépôt) : python .github/scripts/icone_partage.py"""
import glob, os, re

SITE = 'https://www.a2tdistributions.fr'
DEFAUT = 'assets/images/devanture-a2t-distributions-cleguer.jpg'
ICONES = ('  <link rel="icon" href="/favicon.ico" sizes="any">\n'
          '  <link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32.png">\n'
          '  <link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">\n')


def image_page(html, chemin):
    base = os.path.dirname(chemin)
    for src in re.findall(r'(?:src|poster)="([^"]+\.(?:jpe?g|png|webp))"', html) + re.findall(r"url\('([^']+\.(?:jpe?g|png|webp))'\)", html):
        if src.startswith('http') or 'logo' in src or 'favicon' in src:
            continue
        p = os.path.normpath(os.path.join(base, src)).replace('\\', '/')
        if p.startswith('assets/') and os.path.exists(p):
            return p
    return DEFAUT


def traiter(chemin):
    html = open(chemin, encoding='utf-8').read()
    if '<head>' not in html:
        return None
    avant = html
    if 'rel="icon"' not in html:
        html = re.sub(r'(<meta charset="[^"]+">\s*\n)', lambda m: m.group(1) + ICONES, html, count=1)
    if 'og:image' not in html:
        img = SITE + '/' + image_page(html, chemin)
        balises = f'  <meta property="og:image" content="{img}">\n  <meta name="twitter:image" content="{img}">\n'
        html = html.replace('</head>', balises + '</head>', 1)
    if html != avant:
        open(chemin, 'w', encoding='utf-8').write(html)
        return True
    return False


if __name__ == '__main__':
    n = 0
    for f in sorted(glob.glob('*.html') + glob.glob('blog/*.html')):
        if f.startswith('google'):
            continue
        r = traiter(f)
        n += bool(r)
        print(('modifié ' if r else 'inchangé') + ' ' + f)
    print(n, 'pages modifiées')
