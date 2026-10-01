# Portfolio

Static, single-page portfolio showcasing **HomeFix** and **Baseline**. No framework, no dependencies, no tracking.

```
index.html        all content (search for TODO to find what to fill in)
styles.css        all styling, light + dark mode
assets/img/       screenshots (WebP) and app icons
build.mjs         copies the site into ./public for Cloudflare (Node, no deps)
wrangler.jsonc    Cloudflare static-assets Worker
```

## Before publishing — fill in the TODOs in `index.html`
- [ ] Email in the contact `mailto:` link
- [ ] WhatsApp number (`https://wa.me/<digits>`), or delete that button
- [ ] HomeFix live URL (currently `https://homefix.pages.dev`; confirm it)
- [ ] Baseline live URL (currently a placeholder)
- [ ] GitHub link (`habdelkaderr`); make sure the repos you want seen are public

## Preview locally
```bash
python -m http.server 8000      # then open http://localhost:8000
```

## Deploy for free: GitHub Pages (recommended)
No build step and no account other than GitHub. The URL is `https://habdelkaderr.github.io`.
1. On github.com create a **public** repo named exactly `habdelkaderr.github.io`.
2. Push this folder to it:
   ```bash
   git init
   git add .
   git commit -m "Portfolio"
   git branch -M main
   git remote add origin https://github.com/habdelkaderr/habdelkaderr.github.io.git
   git push -u origin main
   ```
3. Repo → **Settings → Pages** → Source: **Deploy from a branch**, Branch: `main`, folder `/ (root)` → Save.
4. Wait about a minute, then open `https://habdelkaderr.github.io`. Every later `git push` updates it.

## Alternative, also free: Cloudflare (same setup as HomeFix and Baseline)
Cloudflare → **Workers & Pages → Create → Workers → Import a repository**, with build command `npm run build` and deploy command `npx wrangler deploy`. The URL is `portfolio.<your-account>.workers.dev`.

A custom domain is optional (about $10/year) and not needed.

## Updating screenshots
Source images live in `../Mech/tests/screenshots/` (HomeFix e2e run) and `../Whoop/build/` (Baseline). Convert new ones to WebP at around quality 82 and keep each under about 150 KB.
