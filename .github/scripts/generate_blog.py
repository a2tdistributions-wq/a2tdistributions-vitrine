#!/usr/bin/env python3
"""
A2T Distributions — Générateur automatique d'articles de blog hebdomadaires.
Appelle Claude API pour choisir un nouveau sujet (en évitant les sujets déjà publiés),
produire un article HTML complet, l'écrire dans blog/, et met à jour blog/index.html.
"""

import anthropic
import os
import random
import re
from datetime import datetime

MOIS_FR = {
    1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
    7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
}

CATEGORIES = [
    "Portes de garage", "Portes d'entrée", "Fenêtres & Baies",
    "Menuiseries", "Conseils", "Solaire", "Bornes de recharge", "Panneaux habitat",
]

# Catégories qui reçoivent le badge vert dans blog/index.html (les autres restent rouge)
GREEN_CATEGORIES = ("Fenêtres & Baies", "Menuiseries", "Conseils", "Solaire", "Bornes de recharge")

# Plusieurs images possibles par catégorie (choisies au hasard pour varier les visuels)
CATEGORY_IMAGES = {
    "Portes de garage": [
        "sectionnelle-noire-lorient-morbihan.jpg", "hormann-sectionnelle-hublots-morbihan.jpg",
        "hormann-double-sectionnelle-portillon.jpg", "double-garage-sectionnelle-ploeumeur.jpg",
        "double-sectionnelle-garage-morbihan.jpg", "double-sectionnelle-wenge-villa-blanche.jpg",
        "sectionnelle-anthracite-hublots-auray.jpg", "sectionnelle-anthracite-plouay-morbihan.jpg",
        "sectionnelle-blanche-maison-neuve.jpg", "sectionnelle-bois-chantier-morbihan.jpg",
        "sectionnelle-bois-mur-pierre-bretagne.jpg", "sectionnelle-brun-maison-bretagne.jpg",
        "sectionnelle-corten-villa-moderne.jpg", "porte-garage-alu-vitree-bretagne.jpg",
    ],
    "Portes d'entrée": [
        "pirnar-q10-anthracite-lanester.jpg", "pirnar-quantum-q10-showroom.jpg",
        "porte-entree-blanche-vitree-granite.jpg", "porte-entree-bois-mur-pierre-bretagne.jpg",
        "porte-pivot-bois-a2t-morbihan.jpg", "porte-pivot-tehni-larmor-plage.jpg",
        "pose-porte-pivot-equipe-a2t.jpg", "chantier-porte-entree-garage-lorient.jpg",
    ],
    "Fenêtres & Baies": [
        "fenetres-alu-chantier-hennebont.jpg", "fenetres-pvc-blanc-maison-granite.jpg",
        "baies-vitrees-noires-briques-terreal.jpg",
    ],
    "Menuiseries": [
        "batiment-a2t-distributions-exterieur.jpg", "devanture-a2t-distributions-cleguer.jpg",
        "depot-a2t-distributions-facade-cleguer.jpg", "porte-aluminium-batiment-pierre-bretagne.jpg",
        "camionnette-livraison-porte-a2t.jpg", "realisation-porte-bois-fenetres-noires.jpg",
        "pergola-aluminium-bioclimatique-bretagne.jpg",
    ],
    "Conseils": [
        "showroom-a2t-catalogues-tehni-pirnar.jpg", "showroom-a2t-pirnar-eclaire.jpg",
        "showroom-a2t-porte-tehni-bois.jpg", "showroom-a2t-tehni-pirnar-table-conseil.jpg",
        "showroom-a2t-vue-ensemble.jpg", "chantier-complet-maison-bretagne.jpg",
        "chantier-maison-contemporaine-a2t.jpg",
    ],
    "Solaire": ["panneaux-solaires-toit-ardoise-bretagne.jpg"],
    "Bornes de recharge": [
        "borne-recharge-v2c-installation-garage.jpg", "borne-recharge-v2c-wallbox-bretagne.jpg",
    ],
    "Panneaux habitat": [
        "chantier-complet-maison-bretagne.jpg", "batiment-a2t-distributions-exterieur.jpg",
    ],
}

SYSTEM_PROMPT = """Tu es un rédacteur SEO expert en menuiseries, habitat et énergie en Bretagne,
travaillant pour A2T Distributions (Cléguér, Morbihan). Tu rédiges des articles de blog HTML
complets, vendeurs, en français naturel, ciblant des requêtes locales bretonnes.

A2T Distributions :
- Portes de garage Hörmann & Flexidoor
- Portes d'entrée Pirnar & Tehni (spécialité porte à pivot)
- Fenêtres & baies vitrées aluminium
- Panneaux solaires photovoltaïques
- Bornes de recharge EV IRVE
- Panneaux habitat sur mesure (pros, hôtels, campings, collectivités) — réseau national de distributeurs en développement
- Zone : Bretagne, Morbihan, Finistère, Ille-et-Vilaine, Loire-Atlantique
- SIREN 853547115 — contact@a2tdistributions.fr — Cléguér (56620)"""


def get_used_titles_and_slugs():
    """Lit les articles déjà publiés pour ne jamais répéter un sujet."""
    slugs = set()
    if os.path.isdir("blog"):
        for f in os.listdir("blog"):
            if f.endswith(".html") and f != "index.html":
                slugs.add(f[:-5])
    titles = []
    index_path = "blog/index.html"
    if os.path.exists(index_path):
        with open(index_path, encoding="utf-8") as f:
            content = f.read()
        titles = re.findall(r'<h2><a href="[^"]+">([^<]+)</a></h2>', content)
    return slugs, titles


def pick_topic(client, used_titles):
    """Demande à Claude un nouveau sujet d'article, distinct de ceux déjà publiés."""
    used_list = "\n".join(f"- {t}" for t in used_titles) or "(aucun article publié pour l'instant)"
    prompt = f"""Propose UN nouveau sujet d'article de blog SEO pour A2T Distributions
(menuiserie/habitat en Bretagne). Le sujet doit être utile, concret, cibler une vraie
requête de recherche locale (prix, comparatif, guide, sécurité, aide financière...).

Catégories possibles (choisis-en UNE exactement, orthographe identique) :
{", ".join(CATEGORIES)}

Sujets déjà publiés — NE PAS répéter ni reformuler légèrement l'un d'entre eux :
{used_list}

Réponds STRICTEMENT sous cette forme, 3 lignes, rien d'autre :
TITRE: <titre accrocheur et précis>
SLUG: <slug-en-minuscules-sans-accents-separe-par-des-tirets>
CATEGORIE: <une des catégories listées ci-dessus>"""

    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    text = resp.content[0].text
    titre = re.search(r"TITRE:\s*(.+)", text).group(1).strip()
    slug = re.search(r"SLUG:\s*(.+)", text).group(1).strip()
    categorie = re.search(r"CATEGORIE:\s*(.+)", text).group(1).strip()
    if categorie not in CATEGORIES:
        categorie = "Conseils"
    return titre, slug, categorie


def generate_html(titre, slug, categorie, mois_fr, annee, image_hero):
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    user_prompt = f"""Génère un article de blog HTML COMPLET sur le sujet : "{titre}"

INSTRUCTIONS STRICTES :

1. Produis UNIQUEMENT le HTML entre les balises <article> et </article> (le contenu de l'article uniquement, pas la page entière — je l'insère moi-même dans le template).

2. Structure requise dans l'article :
   - <div class="article-meta"> avec <span class="article-meta__cat">{categorie}</span>, "Par A2T Distributions · Bretagne", "{mois_fr} {annee} · X min de lecture"
   - <h1 style="font-size:clamp(26px,4vw,40px);font-weight:900;line-height:1.2;margin-bottom:24px;color:var(--dark)"> avec le titre exact
   - 2 à 3 paragraphes intro
   - 3 à 5 sections H2 avec sous-sections H3
   - 1 tableau HTML (<table>) avec des prix indicatifs réalistes (fourchettes)
   - 2 blocs <div class="highlight"> avec contenu utile et 1 lien <a href="../contact.html" style="color:var(--red);font-weight:700">→ Demander un devis</a>
   - Mentions naturelles de : Lorient, Morbihan, Bretagne, Finistère, A2T Distributions
   - 700-900 mots de contenu réel

3. Ton : expert, vendeur sans être agressif, pédagogue, confiance. Français naturel.

4. Données : utilise des fourchettes de prix réalistes pour la France en {annee}. Pas de chiffres inventés précis.

5. NE génère PAS les balises html/head/body/nav/footer — juste le contenu <article>...</article>."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )

    article_content = message.content[0].text

    # Nettoyer les balises markdown code block si Claude en a ajouté
    import re as _re
    article_content = _re.sub(r'^```(?:html)?\s*', '', article_content.strip(), flags=_re.MULTILINE)
    article_content = _re.sub(r'\s*```$', '', article_content.strip(), flags=_re.MULTILINE)
    article_content = article_content.strip()

    # Wrap dans le template complet
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{titre} | A2T Distributions Bretagne</title>
  <meta name="description" content="{titre} — Guide complet par A2T Distributions, spécialiste menuiseries en Bretagne et Morbihan.">
  <link rel="canonical" href="https://a2tdistributions.fr/blog/{slug}.html">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{titre}",
    "author": {{"@type": "Organization", "name": "A2T Distributions"}},
    "publisher": {{"@type": "Organization", "name": "A2T Distributions"}},
    "datePublished": "{datetime.now().strftime('%Y-%m-%d')}",
    "description": "{titre} — Guide complet A2T Distributions Bretagne."
  }}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/style.css">
  <link rel="stylesheet" href="../css/blog.css">
</head>
<body>

  <nav class="nav scrolled" id="nav">
    <div class="container nav__inner">
      <a href="../index.html" class="nav__logo">
        <span class="nav__logo-a">A2T</span> Distributions
      </a>
      <ul class="nav__links" id="navLinks">
        <li><a href="../index.html" class="nav__link">Accueil</a></li>
        <li><a href="../services.html" class="nav__link">Services</a></li>
        <li><a href="../about.html" class="nav__link">À propos</a></li>
        <li><a href="index.html" class="nav__link active">Blog</a></li>
        <li><a href="../contact.html" class="nav__link nav__link--cta">Devis gratuit</a></li>
      </ul>
      <button class="nav__burger" id="burger" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
  </nav>

  <img src="../assets/images/{image_hero}" alt="{titre} — A2T Distributions Bretagne" class="article-hero">

  <div class="container">
    <div class="article-wrap">

      {article_content}

      <aside class="article-sidebar">
        <div class="sidebar-cta">
          <h4>Devis gratuit sous 24h</h4>
          <p>Décrivez votre projet — on vous rappelle et on se déplace en Bretagne.</p>
          <a href="../contact.html" class="btn btn--primary btn--sm" style="width:100%;text-align:center;justify-content:center">Demander un devis →</a>
        </div>
        <div class="sidebar-card">
          <h4>Nos services</h4>
          <ul>
            <li><a href="../services.html#portes-garage">Portes de garage</a></li>
            <li><a href="../services.html#portes-entree">Portes d'entrée</a></li>
            <li><a href="../services.html#fenetres">Fenêtres & Baies</a></li>
            <li><a href="../services.html#solaire">Panneaux solaires</a></li>
            <li><a href="../services.html#bornes-ev">Bornes de recharge EV</a></li>
          </ul>
        </div>
        <div class="sidebar-card">
          <h4>Zones desservies</h4>
          <ul>
            <li>Lorient · Vannes · Auray</li>
            <li>Quimper · Brest · Quimperlé</li>
            <li>Rennes · Nantes · Saint-Brieuc</li>
          </ul>
        </div>
      </aside>
    </div>
  </div>

  <section class="cta-section">
    <div class="container cta-section__inner reveal">
      <h2>Un projet en Bretagne ?</h2>
      <p>A2T Distributions — devis gratuit, déplacement en Morbihan et Finistère.</p>
      <a href="../contact.html" class="btn btn--primary btn--lg">Demander mon devis gratuit →</a>
    </div>
  </section>

  <footer class="footer">
    <div class="container footer__grid">
      <div class="footer__brand">
        <div class="footer__logo"><span class="nav__logo-a">A2T</span> Distributions</div>
        <p>Spécialiste portes, fenêtres, solaire et bornes de recharge en Bretagne.</p>
        <p class="footer__siren">SIREN 853547115</p>
      </div>
      <div class="footer__col"><h4>Navigation</h4><ul><li><a href="../index.html">Accueil</a></li><li><a href="../services.html">Services</a></li><li><a href="../about.html">À propos</a></li><li><a href="index.html">Blog</a></li><li><a href="../contact.html">Contact & Devis</a></li><li><a href="../legal.html">Mentions légales</a></li></ul></div>
      <div class="footer__col"><h4>Blog</h4><ul><li><a href="index.html">Tous les articles</a></li><li><a href="porte-pivot-entree-prix-guide-2026.html">Porte à pivot 2026</a></li><li><a href="pergola-aluminium-bretagne-2026.html">Pergola alu</a></li><li><a href="porte-garage-lorient-2026.html">Portes de garage</a></li><li><a href="panneaux-solaires-bretagne-2026.html">Solaire Bretagne</a></li></ul></div>
    </div>
    <div class="footer__bottom"><div class="container"><p>&copy; {annee} A2T Distributions — <a href="../legal.html">Mentions légales</a></p></div></div>
  </footer>

  <script src="../js/main.js"></script>
</body>
</html>
"""
    return html


def update_blog_index(titre, slug, categorie, mois_fr, annee, image_hero):
    """Insère la nouvelle card en tête de la grille dans blog/index.html"""
    index_path = "blog/index.html"
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    cat_class = ' blog-card__cat--green' if categorie in GREEN_CATEGORIES else ""
    new_card = f"""
        <article class="blog-card reveal">
          <a href="{slug}.html">
            <div class="blog-card__img" style="background-image:url('../assets/images/{image_hero}')"></div>
          </a>
          <div class="blog-card__body">
            <span class="blog-card__cat{cat_class}">{categorie}</span>
            <h2><a href="{slug}.html">{titre}</a></h2>
            <p>Découvrez notre guide complet sur ce sujet clé pour votre habitat en Bretagne.</p>
            <div class="blog-card__footer">
              <span>A2T Distributions</span>
              <span>{mois_fr} {annee} · 5 min</span>
            </div>
          </div>
        </article>
"""
    content = content.replace('<div class="blog-grid">\n', f'<div class="blog-grid">\n{new_card}', 1)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"blog/index.html mis à jour")


def main():
    now = datetime.now()
    annee = now.year
    mois_fr = MOIS_FR[now.month]

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    used_slugs, used_titles = get_used_titles_and_slugs()

    titre, slug, categorie = pick_topic(client, used_titles)

    # Sécurité anti-collision si jamais le slug proposé existe déjà
    if slug in used_slugs:
        slug = f"{slug}-{now.strftime('%Y%m%d')}"

    images = CATEGORY_IMAGES.get(categorie, CATEGORY_IMAGES["Conseils"])
    image_hero = random.choice(images)

    print(f"Sujet choisi : {titre} ({categorie})")

    filepath = f"blog/{slug}.html"
    html = generate_html(titre, slug, categorie, mois_fr, annee, image_hero)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Fichier créé : {filepath}")

    update_blog_index(titre, slug, categorie, mois_fr, annee, image_hero)
    print(f"✅ Article '{titre}' prêt pour commit.")


if __name__ == "__main__":
    main()
