---
title: Esimerkkiprojekti
description: Näyttää kaikki front matter -kentät, jotka pohja ymmärtää.
date: 2026-01-01
tags: [esimerkki, markdown]
downloads:
  - label: Esimerkki-PDF (laita tiedosto kansioon assets/files)
    href: /assets/files/example.pdf
links:
  - label: Markdown-syntaksi
    href: https://daringfireball.net/projects/markdown/syntax
images: []
---

# Esimerkkiprojekti

Kopioi tämä tiedosto, kun aloitat uuden projektisivun.

## Taulukko

| Vaihe | Mitä             | Missä             |
| ----- | ---------------- | ----------------- |
| 1     | Kirjoita teksti  | `content/*.md`    |
| 2     | Lisää valikkoon  | `settings.json`   |
| 3     | Rakenna          | `python build.py` |

## Kuva

Laita `kuva.png` kansioon `assets/img` ja kirjoita:

```
![Kuvan kuvaus](/assets/img/kuva.png)
```

## YouTube-video

Markdown päästää HTML:n läpi. Liitä YouTuben Jaa, Upota -valikon koodi.
Video latautuu silloin YouTubesta ja asettaa sen evästeet.
Mainitse se tietosuojasivulla.
