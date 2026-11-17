# Smart Mountains website (smartmountains.net)

Static site, EN and IT. A Fab Campaigns concept. Draft 1.

## Deploy on Cloudflare Pages (from GitHub)

1. Push this repo to GitHub.
2. Cloudflare dashboard > Workers & Pages > Create > Pages > Connect to Git, pick the repo.
3. Framework preset: None. Build command: leave empty. Build output directory: `public`.
4. Custom domains: add `smartmountains.net` and `www.smartmountains.net`.
5. Before switching DNS, export or note the WordPress content you want to keep, and keep WordPress running until the Pages site is live on the domain.

`public/_redirects` maps old WordPress URLs to the new ones. `public/_headers` sets security headers and a strict Content-Security-Policy (no third-party scripts, fonts or analytics are loaded). If you add analytics or a form service later, extend the CSP there.

## Structure

- `public/` is the whole site: `index.html`, `about/`, `partner-with-us/`, and the Italian pages under `it/`.
- `public/assets/` holds CSS, a small menu script, self-hosted fonts (Source Serif 4, Raleway, Poppins, all SIL OFL) and the share image.
- `tools/build.py` is optional. It regenerates the HTML so the header, footer and copy in both languages can be edited in one place. Edit the HTML directly if you prefer.

## Open items

- Replace the ridgeline artwork with photography where you have permission to use it (pilot sites only once the local authority agrees).
- Italian copy is a first pass for review by a native reader.
- Footer legal line (Fab Campaigns Ltd, company number) to be verified before going live.
