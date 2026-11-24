# Site source

The live site (https://sangmin2-rf.github.io) is the static HTML in `../site/`,
deployed by `.github/workflows/static-site.yml` on every push that touches `site/`.

## Update workflow
1. Edit `data.py` (publications, news, awards, projects, ...).
2. Run `python build.py` -> regenerates `docs/` (HTML/CSS/JS inlined, plus llms.txt, sitemap.xml).
3. Upload the generated files from `docs/` into the repo's `site/` folder (photo lives in `site/assets/prof_pic.jpg`).

The al-folio files at the repo root are no longer served (Pages source = GitHub Actions).
