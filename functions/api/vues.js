// Compteur de vues du blog .fr (14/11/2026).
// GET  /api/vues?p=slug1,slug2  -> {"slug1": 12, "slug2": 40}
// POST /api/vues?p=slug         -> compte une lecture (appelé par js/main.js, une fois par visiteur et par 12 h)
const SLUG = /^[a-z0-9-]{3,120}$/;
const ROBOT = /bot|crawl|spider|slurp|preview|facebookexternalhit|headless|lighthouse|python|curl|wget|httpclient/i;

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}

async function articleExiste(env, request, slug) {
  // sans 404.html, Pages renvoie l'accueil (200) pour une adresse inconnue : on vérifie que c'est bien un article
  const r = await env.ASSETS.fetch(new Request(new URL(`/blog/${slug}`, request.url)));
  return r.status === 200 && (await r.text()).includes('class="article-meta"');
}

export async function onRequestGet({ request, env }) {
  const p = (new URL(request.url).searchParams.get("p") || "").split(",").filter((s) => SLUG.test(s)).slice(0, 60);
  const vals = await Promise.all(p.map((s) => env.VUES.get("v:" + s)));
  const out = {};
  p.forEach((s, i) => (out[s] = parseInt(vals[i] || "0", 10)));
  return json(out);
}

export async function onRequestPost({ request, env }) {
  const slug = new URL(request.url).searchParams.get("p") || "";
  if (!SLUG.test(slug) || slug === "index") return json({ erreur: "article inconnu" }, 400);
  if (ROBOT.test(request.headers.get("user-agent") || "")) return json({ ignore: "robot" });
  if (!(await articleExiste(env, request, slug))) return json({ erreur: "article inconnu" }, 404);
  const n = parseInt((await env.VUES.get("v:" + slug)) || "0", 10) + 1;
  await env.VUES.put("v:" + slug, String(n));
  return json({ [slug]: n });
}
