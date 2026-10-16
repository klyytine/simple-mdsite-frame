#!/usr/bin/env python3
"""simple-mdsite-frame: a small static site generator.

Reads settings.json and content/<slug>.<lang>.md, writes a finished site to dist/.
The default language (settings.json "default_lang") lands at the site root,
other languages under /<lang>/. Internal links are written relative, so
dist/ also works when opened straight from disk. No JavaScript is emitted.

Usage:
    python build.py [--out dist] [--serve] [--port 8000]
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
ASSETS = ROOT / "assets"
SETTINGS = ROOT / "settings.json"

# Interface words per language. Add a block here when you add a language.
UI = {
    "en": {
        "nav_label": "Site sections",
        "menu_label": "Menu",
        "meta_label": "Page details",
        "updated_label": "Updated",
        "downloads": "Downloads",
        "links": "Links",
        "published": "Published",
        "lang_label": "Language",
    },
    "fi": {
        "nav_label": "Sivuston osat",
        "menu_label": "Valikko",
        "meta_label": "Sivun tiedot",
        "updated_label": "Päivitetty",
        "downloads": "Lataukset",
        "links": "Linkit",
        "published": "Julkaistu",
        "lang_label": "Kieli",
    },
}


@dataclass
class Page:
    slug: str
    lang: str
    title: str
    meta: dict
    body_html: str


def fail(msg: str) -> None:
    print(f"build.py: error: {msg}", file=sys.stderr)
    raise SystemExit(1)


def read_settings() -> dict:
    if not SETTINGS.exists():
        fail(f"{SETTINGS.name} not found")
    try:
        return json.loads(SETTINGS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"{SETTINGS.name} line {e.lineno} column {e.colno}: {e.msg}")


def split_front_matter(text: str, name: str) -> tuple[dict, str]:
    """Return (front matter dict, markdown body)."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as e:
        fail(f"front matter in {name} is not valid YAML: {e}")
    if not isinstance(meta, dict):
        fail(f"front matter in {name} must be key: value lines")
    return meta, parts[2].lstrip("\n")


def load_page(slug: str, lang: str) -> Page | None:
    path = CONTENT / f"{slug}.{lang}.md"
    if not path.exists():
        return None
    meta, body = split_front_matter(path.read_text(encoding="utf-8"), path.name)
    md = markdown.Markdown(extensions=["tables", "attr_list", "toc", "sane_lists"])
    return Page(slug=slug, lang=lang, title=str(meta.get("title", slug)),
                meta=meta, body_html=md.convert(body))


def flatten(nav: list, depth: int = 0) -> list:
    out = []
    for item in nav:
        out.append((item, depth))
        out.extend(flatten(item.get("children", []), depth + 1))
    return out


def page_url(slug: str, lang: str, default_lang: str) -> str:
    prefix = "" if lang == default_lang else f"{lang}/"
    name = "index.html" if slug == "index" else f"{slug}.html"
    return f"/{prefix}{name}"


def root_prefix(lang: str, default_lang: str) -> str:
    return "" if lang == default_lang else "../"


def label_for(item: dict, lang: str, default_lang: str) -> str:
    titles = item.get("title", {})
    return html.escape(titles.get(lang, titles.get(default_lang, item["slug"])))


def render_tree(nav: list, lang: str, default_lang: str, current: str) -> str:
    def render(items: list, level: int) -> str:
        visible = [i for i in items if i.get("visible") and not i.get("footer_only")]
        if not visible:
            return ""
        css = ' class="children"' if level else ""
        rows = []
        for item in visible:
            slug = item["slug"]
            cls = ' class="current"' if slug == current else ""
            kids = render(item.get("children", []), level + 1)
            href = html.escape(page_url(slug, lang, default_lang))
            rows.append(f'<li><a href="{href}"{cls}>{label_for(item, lang, default_lang)}</a>{kids}</li>')
        return f"<ul{css}>" + "".join(rows) + "</ul>"

    return render(nav, 0)


def render_lang_switch(slug: str, lang: str, languages: list, default_lang: str) -> str:
    if len(languages) < 2:
        return ""
    links = []
    for code in languages:
        cls = ' class="active"' if code == lang else ""
        href = html.escape(page_url(slug, code, default_lang))
        links.append(f'<a href="{href}"{cls} hreflang="{code}">{code.upper()}</a>')
    return '<span class="sep">/</span>'.join(links)


def render_meta(page: Page, t: dict) -> str:
    blocks = []

    date = page.meta.get("date")
    tags = page.meta.get("tags") or []
    if date or tags:
        inner = []
        if date:
            inner.append(f'<p>{t["published"]} {html.escape(str(date))}</p>')
        if tags:
            chips = "".join(f"<span>{html.escape(str(x))}</span>" for x in tags)
            inner.append(f'<div class="tags">{chips}</div>')
        blocks.append("<section>" + "".join(inner) + "</section>")

    for key in ("downloads", "links"):
        items = page.meta.get(key) or []
        if not items:
            continue
        rows = []
        for item in items:
            href = html.escape(str(item.get("href", "#")))
            text = html.escape(str(item.get("label", href)))
            rows.append(f'<li><a href="{href}">{text}</a></li>')
        blocks.append(f"<section><h2>{t[key]}</h2><ul>" + "".join(rows) + "</ul></section>")

    images = page.meta.get("images") or []
    if images:
        rows = []
        for item in images:
            src = html.escape(str(item.get("src", "")))
            alt = html.escape(str(item.get("alt", "")))
            rows.append(f'<figure><img src="{src}" alt="{alt}" loading="lazy"></figure>')
        blocks.append("<section>" + "".join(rows) + "</section>")

    return "\n".join(blocks)


def render_contact(site: dict) -> str:
    parts = []
    email = site.get("email")
    if email:
        e = html.escape(email)
        parts.append(f'<a href="mailto:{e}">{e}</a>')
    for link in site.get("contact_links", []):
        href = html.escape(str(link.get("href", "")))
        text = html.escape(str(link.get("label", href)))
        parts.append(f'<a href="{href}" rel="me noopener">{text}</a>')
    return '<span class="sep">&middot;</span>'.join(parts)


def render_footer_links(nav: list, lang: str, default_lang: str) -> str:
    rows = []
    for item, _ in flatten(nav):
        if not item.get("footer_only") or not item.get("visible"):
            continue
        href = html.escape(page_url(item["slug"], lang, default_lang))
        rows.append(f'<a href="{href}">{label_for(item, lang, default_lang)}</a>')
    return " ".join(rows)


def fill(template: str, values: dict) -> str:
    out = template
    for key, value in values.items():
        out = out.replace("{{" + key + "}}", str(value))
    return out


SITE_PATH = re.compile(r'(\b(?:href|src)=")/(?!/)')


def relativize(page_html: str, root: str) -> str:
    """Turn site-absolute links (/x) into relative ones, so file:// works too."""
    return SITE_PATH.sub(lambda m: m.group(1) + (root or "./"), page_html)


def localized(value, lang: str, default_lang: str) -> str:
    """Settings values may be a plain string or {"en": ..., "fi": ...}."""
    if isinstance(value, dict):
        return str(value.get(lang, value.get(default_lang, "")))
    return str(value or "")


def build(out_dir: Path) -> int:
    settings = read_settings()
    site = settings["site"]
    nav = settings["nav"]
    default_lang = site["default_lang"]
    languages = site["languages"]
    domain = (site.get("domain") or "").strip()
    base = (TEMPLATES / "base.html").read_text(encoding="utf-8")
    build_date = dt.date.today().isoformat()

    for lang in languages:
        if lang not in UI:
            fail(f'language "{lang}" has no UI block in build.py, copy the "en" block and translate it')

    if out_dir.exists():
        # Keep .git so the output folder can double as a publish repository.
        for child in out_dir.iterdir():
            if child.name == ".git":
                continue
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    out_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    missing = []

    for lang in languages:
        t = UI[lang]
        for item, _ in flatten(nav):
            if not item.get("visible"):
                continue
            slug = item["slug"]
            page = load_page(slug, lang)
            if page is None:
                missing.append(f"{slug}.{lang}.md")
                continue

            tagline = localized(site.get("tagline"), lang, default_lang)
            values = {
                "lang": lang,
                "root": root_prefix(lang, default_lang),
                "page_title": html.escape(page.title),
                "site_title": html.escape(localized(site.get("title"), lang, default_lang)),
                "site_tagline": html.escape(tagline),
                "description": html.escape(str(page.meta.get("description", tagline))),
                "home_url": page_url("index", lang, default_lang),
                "lang_switch": render_lang_switch(slug, lang, languages, default_lang),
                "tree": render_tree(nav, lang, default_lang, slug),
                "content": page.body_html,
                "meta": render_meta(page, t),
                "contact": render_contact(site),
                "footer_links": render_footer_links(nav, lang, default_lang),
                "build_date": build_date,
                "nav_label": t["nav_label"],
                "menu_label": t["menu_label"],
                "meta_label": t["meta_label"],
                "updated_label": t["updated_label"],
                "lang_label": t["lang_label"],
            }

            rel = page_url(slug, lang, default_lang).lstrip("/")
            target = out_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(relativize(fill(base, values), values["root"]), encoding="utf-8")
            written += 1

    if ASSETS.exists():
        shutil.copytree(ASSETS, out_dir / "assets")

    (out_dir / ".nojekyll").write_text("", encoding="utf-8")

    if domain:
        # Branch-based GitHub Pages publishing needs CNAME on every deploy,
        # or the custom domain is dropped. The Actions artifact deploy ignores it.
        (out_dir / "CNAME").write_text(domain + "\n", encoding="utf-8")
        urls = []
        for lang in languages:
            for item, _ in flatten(nav):
                if item.get("visible") and (CONTENT / f"{item['slug']}.{lang}.md").exists():
                    urls.append(f"https://{domain}{page_url(item['slug'], lang, default_lang)}")
        (out_dir / "sitemap.txt").write_text("\n".join(urls) + "\n", encoding="utf-8")
        robots = f"User-agent: *\nAllow: /\nSitemap: https://{domain}/sitemap.txt\n"
    else:
        robots = "User-agent: *\nAllow: /\n"
    (out_dir / "robots.txt").write_text(robots, encoding="utf-8")

    print(f"build.py: wrote {written} pages to {out_dir}")
    for name in missing:
        print(f"build.py: note: no translation file {name}, page skipped for that language")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="dist")
    ap.add_argument("--serve", action="store_true", help="serve the output on localhost")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()

    out_dir = (ROOT / args.out).resolve()
    code = build(out_dir)
    if code == 0 and args.serve:
        import functools
        import http.server
        import socketserver
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(out_dir))
        with socketserver.TCPServer(("", args.port), handler) as srv:
            print(f"serving on http://localhost:{args.port} (Ctrl+C to stop)")
            srv.serve_forever()
    return code


if __name__ == "__main__":
    raise SystemExit(main())
