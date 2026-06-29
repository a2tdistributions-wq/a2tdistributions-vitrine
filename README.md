# A2T Distributions — Vitrine

Site vitrine statique pour **a2tdistributions.fr**  
Stack : HTML5 + CSS3 + Vanilla JS | Hébergement : Netlify (gratuit)

## Structure

```
a2tdistributions-vitrine/
├── index.html        → Accueil
├── services.html     → Services (portes, fenêtres, solaire, bornes EV)
├── about.html        → À propos / équipe
├── contact.html      → Formulaire de devis (Formspree)
├── legal.html        → Mentions légales RGPD
├── css/style.css     → Design complet (responsive, animations)
└── js/main.js        → Nav scroll, reveal, compteurs animés
```

## Mise en ligne (1 fois)

1. Créer repo GitHub, pousser ce dossier
2. Sur netlify.com → "Add new site" → "Import from GitHub"
3. Build : aucun | Publish directory : `.` (racine)
4. URL temporaire : `a2tdistributions.netlify.app`

## Lier le domaine OVH

Chez OVH dans "Noms de domaine" → `a2tdistributions.fr` → DNS :
- Supprimer l'enregistrement A existant sur `@`
- Ajouter CNAME : `@` → `a2tdistributions.netlify.app`
- Propagation : 1h à 24h

Sur Netlify : "Domain settings" → ajouter `a2tdistributions.fr` → SSL auto (Let's Encrypt)

## Formulaire de contact

1. Aller sur [formspree.io](https://formspree.io) → créer compte gratuit
2. Créer un nouveau formulaire → copier l'ID (ex: `xrgwqkpz`)
3. Dans `contact.html`, remplacer `YOUR_FORM_ID` par votre ID
4. Les emails arrivent directement sur a2tdistributions@gmail.com

## SEO maillage géographique

Zones ciblées dans le structured data et le contenu :
- Bretagne : Lorient, Vannes, Quimper, Brest, Rennes, Saint-Brieuc
- Pays de la Loire : Nantes, Saint-Nazaire, La Baule, Angers
- Façade Atlantique : La Rochelle, Cholet, Laval
