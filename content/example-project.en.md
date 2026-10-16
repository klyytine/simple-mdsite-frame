---
title: Example project
description: Shows every front matter field the template understands.
date: 2026-01-01
tags: [example, markdown]
downloads:
  - label: Example PDF (put the file in assets/files)
    href: /assets/files/example.pdf
links:
  - label: Markdown syntax
    href: https://daringfireball.net/projects/markdown/syntax
images: []
---

# Example project

Copy this file to start a new project page.

## A table

| Step | What          | Where             |
| ---- | ------------- | ----------------- |
| 1    | Write text    | `content/*.md`    |
| 2    | Add to menu   | `settings.json`   |
| 3    | Build         | `python build.py` |

## An image

Put `picture.png` in `assets/img`, then write:

```
![Description of the picture](/assets/img/picture.png)
```

## A YouTube video

Markdown passes HTML through. Paste the embed code from YouTube's Share, Embed menu.
Note that the video then loads from YouTube and sets its cookies.
Mention it on your privacy page.
