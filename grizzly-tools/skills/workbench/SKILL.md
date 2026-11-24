---
name: workbench
description: Create an interactive diagram or browser tool as a self-contained HTML bundle in a personal workbench server (~/workbench/tools/), where it auto-indexes on the home page and live-reloads. Trigger when the user asks for an interactive diagram, visualization, chart, dashboard, calculator, explorer, or any "tool I can open in a browser" — or says "add this to my workbench", "make a workbench tool", "put this on the workbench", or "/workbench". Use this instead of writing a one-off HTML file to a random path.
---

# Workbench Tool Authoring

The workbench is a personal zero-dependency web server at `~/workbench/` (built on system `python3`). It serves self-contained HTML/JS/CSS bundles from `~/workbench/tools/`, auto-generates a home page that indexes them, and live-reloads any open tab when a file changes at **http://localhost:8765**.

> **First time?** If `~/workbench/` does not exist yet, read `SETUP.md` in the directory containing this `SKILL.md` and run the setup before writing any tools.

## Steps

1. **Pick a kebab-case name** for the tool (e.g. `sdlc-pipeline`, `pricing-explorer`).
2. **Choose single-file vs folder:**
   - **Single file (default):** `~/workbench/tools/<name>.html` with HTML, CSS, and JS inline.
   - **Folder:** `~/workbench/tools/<name>/index.html` plus sibling `.js`/`.css`/asset files, only when the tool genuinely benefits from separate files. It still appears as one tool on the home page.
3. **Write the bundle** with your file-writing tool:
   - Include a meaningful `<title>` — the home page uses it as the tool's label.
   - Make it self-contained; CDN `<script>`/`<link>` tags (D3, Mermaid, Chart.js, etc.) are fine.
   - Do **not** add a live-reload script — the server injects one automatically.
   - Match the dark workbench palette when reasonable (bg `#0f1116`, cards `#161922`, border `#262a36`, accent `#4c7dff`) unless asked otherwise.
4. **Do not start or restart the server.** Writing the file is enough — it appears on the home page and reloads open tabs within ~1s.
5. **Report the URL:** `http://localhost:8765/<name>.html` (or `http://localhost:8765/<name>/`).

## Notes

- Tools live only in `~/workbench/tools/`, never in a shared repo or temp path.
- This is a personal scratch space for quick visuals and explorers, separate from formal deliverables.
