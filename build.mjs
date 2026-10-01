// Copies the static site into ./public for Cloudflare to serve. No dependencies.
import { cpSync, rmSync, mkdirSync, writeFileSync } from "node:fs";

rmSync("public", { recursive: true, force: true });
mkdirSync("public");
for (const f of ["index.html", "styles.css", "assets"]) cpSync(f, `public/${f}`, { recursive: true });
writeFileSync("public/_headers", `/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
/assets/*
  Cache-Control: public, max-age=604800
`);
writeFileSync("public/robots.txt", "User-agent: *\nAllow: /\n");
console.log("Built ./public");
