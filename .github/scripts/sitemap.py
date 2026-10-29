"""Régénère sitemap.xml (URLs propres, sans .html : Cloudflare Pages redirige les .html en 308).
Toutes les pages indexables + tous les articles du blog. Relançable : python .github/scripts/sitemap.py"""
import glob, os, re, subprocess, datetime

D = "https://www.a2tdistributions.fr"
EXCLUS = {"merci", "legal"}  # pages en noindex
PRIO = {"index": "1.0", "services": "0.9", "lorient": "0.9", "lanester": "0.9", "contact": "0.8", "blog/index": "0.8"}

def lastmod(f):
    d = subprocess.run(["git", "log", "-1", "--format=%cs", "--", f], capture_output=True, text=True).stdout.strip()
    return d or datetime.date.today().isoformat()

def url(n):
    if n == "index": return D + "/"
    if n == "blog/index": return D + "/blog/"
    return f"{D}/{n}"

fichiers = sorted(glob.glob("*.html")) + ["blog/index.html"] + sorted(f for f in glob.glob("blog/*.html") if not f.endswith("index.html"))
lignes = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for f in fichiers:
    f = f.replace(os.sep, "/")
    n = f[:-5]
    if n in EXCLUS or n.startswith("google"): continue
    s = open(f, encoding="utf-8").read()
    if re.search(r'<meta name="robots" content="[^"]*noindex', s): continue
    prio = PRIO.get(n, "0.6" if n.startswith("blog/") else "0.7")
    lignes.append(f"  <url><loc>{url(n)}</loc><lastmod>{lastmod(f)}</lastmod><priority>{prio}</priority></url>")
lignes.append("</urlset>")
open("sitemap.xml", "w", encoding="utf-8", newline="\n").write("\n".join(lignes) + "\n")
print(f"sitemap.xml : {len(lignes) - 3} URL")
