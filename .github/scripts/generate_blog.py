#!/usr/bin/env python3
"""
A2T Distributions — Générateur automatique d'articles de blog mensuels
Appelle Claude API pour produire un article HTML complet, l'écrit dans blog/,
et met à jour blog/index.html.
"""

import anthropic
import os
import re
from datetime import datetime

# Planning des sujets par mois
TOPICS = {
    1:  ("Double vitrage ou triple vitrage : lequel choisir en Bretagne ?",
         "double-vs-triple-vitrage-bretagne", "Fenêtres & Baies", ""),
    2:  ("Baie vitrée coulissante ou galandage : avantages et prix 2027",
         "baie-vitree-coulissante-galandage-bretagne", "Fenêtres & Baies", ""),
    3:  ("Porte d'entrée : combien ça coûte vraiment ? (guide prix 2027)",
         "porte-entree-prix-guide-2027", "Portes d'entrée", ""),
    4:  ("Sécurité porte d'entrée : RC2, A2P, multipoints — ce qu'il faut savoir",
         "securite-porte-entree-rc2-a2p-bretagne", "Portes d'entrée", ""),
    5:  ("Volets roulants aluminium en Bretagne : prix et installation 2027",
         "volets-roulants-aluminium-bretagne-2027", "Fenêtres & Baies", ""),
    6:  ("Rénovation menuiserie : par où commencer et comment la financer",
         "renovation-menuiserie-bretagne-guide", "Conseils", ""),
    7:  ("Double vitrage ou triple vitrage : lequel choisir en Bretagne ?",
         "double-vs-triple-vitrage-bretagne", "Fenêtres & Baies", ""),
    8:  ("Portail aluminium sur-mesure : tendances et prix 2027",
         "portail-aluminium-sur-mesure-bretagne-2027", "Menuiseries", ""),
    9:  ("Porte d'entrée aluminium ou PVC : que choisir en 2027 ?",
         "porte-entree-aluminium-vs-pvc-2027", "Portes d'entrée", ""),
    10: ("Porte de garage motorisée : guide complet 2027",
         "porte-garage-motorisee-guide-2027", "Portes de garage", ""),
    11: ("Isolation thermique RE2020 : fenêtres et baies en Bretagne",
         "isolation-thermique-re2020-fenetres-bretagne", "Fenêtres & Baies", ""),
    12: ("Hörmann LPU 67 vs LPU 42 : quelle porte de garage choisir ?",
         "hormann-lpu-67-vs-lpu-42-comparatif", "Portes de garage", ""),
}

MOIS_FR = {
    1:"Janvier", 2:"Février", 3:"Mars", 4:"Avril", 5:"Mai", 6:"Juin",
    7:"Juillet", 8:"Août", 9:"Septembre", 10:"Octobre", 11:"Novembre", 12:"Décembre"
}

# Choisir une image hero existante selon la catégorie
CATEGORY_IMAGES = {
    "Portes de garage": "sectionnelle-noire-lorient-morbihan.jpg",
    "Portes d'entrée":  "pirnar-q10-anthracite-lanester.jpg",
    "Fenêtres & Baies": "fenetres-alu-chantier-hennebont.jpg",
    "Menuiseries":      "batiment-a2t-distributions-exterieur.jpg",
    "Conseils":         "showroom-a2t-catalogues-tehni-pirnar.jpg",
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
- Zone : Bretagne, Morbihan, Finistère, Ille-et-Vilaine, Loire-Atlantique
- SIREN 853547115 — contact@a2tdistributions.fr — Cléguér (56620)"""


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

    # Couleur de badge selon catégorie
    cat_class = ""
    if categorie in ("Fenêtres & Baies", "Menuiseries", "Conseils"):
        cat_class = ' blog-card__cat--green'

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
    # Insère après l'ouverture de la grille
    content = content.replace('<div class="blog-grid">\n', f'<div class="blog-grid">\n{new_card}', 1)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"blog/index.html mis à jour")


def main():
    now = datetime.now()
    month = now.month
    annee = now.year
    mois_fr = MOIS_FR[month]

    titre, slug, categorie, _ = TOPICS[month]
    image_hero = CATEGORY_IMAGES.get(categorie, "showroom-a2t-catalogues-tehni-pirnar.jpg")

    # Vérifier si l'article existe déjà
    filepath = f"blog/{slug}.html"
    if os.path.exists(filepath):
        print(f"Article {filepath} déjà existant — skip.")
        return

    print(f"Génération : {titre}")
    html = generate_html(titre, slug, categorie, mois_fr, annee, image_hero)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Fichier créé : {filepath}")

    update_blog_index(titre, slug, categorie, mois_fr, annee, image_hero)
    print(f"✅ Article '{titre}' prêt pour commit.")


if __name__ == "__main__":
    main()
