# Fonts

## What ships here

**Public Sans**, weights 400 and 700, Latin subset, WOFF2.

- Designers: The Public Sans Project Authors, https://github.com/uswds/public-sans
- Files from the npm package `@fontsource/public-sans` 5.1.1, https://fontsource.org/fonts/public-sans
- License: SIL Open Font License 1.1, see `OFL.txt` in this folder.

Public Sans is a neutral sans-serif in the same family of styles as Inter.
It is self-hosted, so visitors' browsers make no request to Google or any other font service.

The Latin subset covers English, Finnish, Swedish and most Western European languages.
For other scripts, download the matching subset from Fontsource.

## Using Inter instead

Inter is also licensed under the SIL Open Font License 1.1.

1. Download the files from one of these:
   - Fontsource: https://fontsource.org/fonts/inter (click Download)
   - The Inter project: https://github.com/rsms/inter/releases
2. Copy `inter-latin-400-normal.woff2` and `inter-latin-700-normal.woff2` into this folder.
3. Copy Inter's license file here too, named `OFL-Inter.txt`. The license requires it to travel with the font.
4. Open `assets/css/site.css`. In both `@font-face` blocks:
   - change `font-family: "Public Sans";` to `font-family: Inter;`
   - change the file name in `src: url(...)` to the Inter file
5. In `:root`, change `--font: "Public Sans", ...` to `--font: Inter, ...`.
6. Build again and reload the page with Ctrl+F5.

If you remove Public Sans, delete its two `.woff2` files and `OFL.txt` together.
