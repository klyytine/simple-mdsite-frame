# simple-mdsite-frame

A small static website frame. You write Markdown, one Python script writes HTML.
No JavaScript, no cookies, no external requests, no framework to keep updated.

- Five-part layout: header, menu tree, content, details column, footer
- Desktop: three columns. Mobile: one column with a fold-out menu
- Two languages out of the box (EN and FI), more can be added
- One settings file controls the menu and what is visible
- Self-hosted open-license font (Public Sans)
- Publishes to GitHub Pages for free, with an optional custom domain

New to git and Python? Start with **[docs/ABC_GUIDE.md](docs/ABC_GUIDE.md)**.

## Quick start

```bash
python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
python build.py --serve        # open http://localhost:8000, stop with Ctrl+C
```

The finished site is in `dist/`. Opening `dist/index.html` from disk also works.

## Folder layout

| Path                              | What it is                                                  |
| --------------------------------- | ----------------------------------------------------------- |
| `settings.json`                   | Site title, languages, contact links, menu tree, visibility |
| `content/<slug>.<lang>.md`        | Page text, one file per page per language                   |
| `templates/base.html`             | The single page template                                    |
| `assets/css/site.css`             | All styling. Colours are at the top                         |
| `assets/img`, `assets/files`      | Images and downloadable files                               |
| `assets/fonts`                    | Font files and their license                                |
| `build.py`                        | The generator                                               |
| `.github/workflows/deploy.yml`    | Publishing, option A                                        |
| `docs/optional/deploy-two-repo.yml` | Publishing, option B                                      |
| `dist/`                           | Build output. Never edit by hand, never commit              |

## Everyday tasks

**Add a page**

1. Add an entry to `nav` in `settings.json`. A sub-page goes in the parent's `children` list.
2. Create `content/<slug>.en.md` and `content/<slug>.fi.md`. Copy `example-project.*.md` as a start.
3. Run `python build.py --serve` and check both languages.

**Hide a page:** set `"visible": false`. The files can stay.

**Footer-only page** (privacy, imprint): set `"footer_only": true`.

**Change colours:** edit the variables in `:root` at the top of `assets/css/site.css`.

**Change the font:** see [assets/fonts/README.md](assets/fonts/README.md), which also explains how to switch to Inter.

## Front matter

The lines between the two `---` at the top of a page fill the right-hand column.

```yaml
---
title: Page title            # browser tab and heading
description: One sentence.   # search engines and link previews
date: 2026-01-01             # shown as "Published"
tags: [one, two]
downloads:
  - label: My CV (PDF)
    href: /assets/files/cv.pdf
links:
  - label: Project on GitHub
    href: https://github.com/you/project
images:
  - src: /assets/img/picture.png
    alt: What the picture shows
---
```

Write internal links from the site root: `/about.html` for the default language,
`/fi/about.html` for the others. `build.py` turns them into relative links.

## Publishing

| Option | Repositories                                    | When to pick it                                        | Guide                                                     |
| ------ | ----------------------------------------------- | ------------------------------------------------------ | --------------------------------------------------------- |
| A      | One public repo, source and site together       | Default. Simplest. Your Markdown is public anyway      | [docs/ABC_GUIDE.md](docs/ABC_GUIDE.md), part 6            |
| B      | Private source repo, public output repo         | You want drafts, notes or history kept private         | [docs/TWO_REPO_DEPLOY.md](docs/TWO_REPO_DEPLOY.md)        |

On the free GitHub plan, Pages only publishes from public repositories.
Option B is the way to keep the source private within that rule.

Custom domain: [docs/CUSTOM_DOMAIN.md](docs/CUSTOM_DOMAIN.md).

## When something breaks

[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) lists symptoms, causes and fixes.

## Before you publish

- Replace every placeholder in `settings.json` and `content/`.
- Never put passwords, tokens or keys in this folder. Everything in a public repo is public.
- Anything you add to `content/` and `assets/` will be readable by anyone.

## License

Code and documentation: MIT, see [LICENSE](LICENSE).
Fonts: SIL Open Font License 1.1, see [assets/fonts/OFL.txt](assets/fonts/OFL.txt).
