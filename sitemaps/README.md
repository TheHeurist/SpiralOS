# Domain-specific sitemap publishing

This directory holds alternate sitemap payloads for domains that point to SpiralOS content (e.g., `conjugate-intelligence.com`, `.org`, `.net`, `.de`).

## How to clone the existing sitemap for another host
1. Ensure the root `sitemap.xml` is current.
2. Run the helper script, substituting your target host:

   ```bash
   node scripts/clone-sitemap.js \
     --host https://conjugate-intelligence.com \
     --source sitemap.xml \
     --output sitemaps/conjugate-intelligence.com.xml
   ```

   The helper infers the `--from` host from the first `<loc>` entry in `sitemap.xml`; provide `--from` explicitly if you want to clone from another base.

3. Point the DNS-backed host at the generated sitemap path (or copy it to the corresponding deployment bucket), and update the host-specific `robots.txt` to advertise it.

## Notes
- The script performs a host swap only; if a domain serves a reduced subset of pages, delete unneeded `<url>` entries after generation.
- Use the same process for additional domains (e.g., `.org`, `.net`, `.de`) by swapping the `--host` and `--output` arguments.
- Keep this directory under version control so that published sitemap payloads stay auditable and easy to refresh.
