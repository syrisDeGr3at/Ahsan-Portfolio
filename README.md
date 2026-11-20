# Ahsan Rehman — portfolio

## Deploy (Vercel)
1. Copy everything in this folder into the root of your existing portfolio repo.
   - It replaces: index.html, legalmind.html, taskflow.html, ledger.html, textcraft.html
   - It adds: legal.html, css/, js/, vendor/ (replace the whole css/ js/ vendor/ folders if you uploaded an older version)
   - KEEP your existing `assets/` and `apps/` folders — the site uses them
     (assets/ahsan-formal.webp, assets/legalmind/*.webp, assets/*.jpg, apps/*.html).
2. Delete the old about.html / projects.html / resume.html / contact.html if you no longer want them.
3. Push. Vercel redeploys automatically.

## Hero portrait (important)
The hero shows `assets/ahsan-cutout.png` if it exists: a PNG of you with the background removed
(transparent), like the reference site. Until you add it, the site uses `assets/ahsan-formal.webp`
in black and white with soft faded edges.

## Preview locally
Open a terminal in the folder and run `python -m http.server 8000`, then visit http://localhost:8000
(Double-clicking index.html won't run the 3D card, because browsers block JS modules on file://.
The site falls back to a flat card in that case.)

## Editing content
All text lives in the HTML files. To change pages in bulk, edit the data at the top of build.py
and run `python build.py` from this folder (it writes the .html files next to it).
