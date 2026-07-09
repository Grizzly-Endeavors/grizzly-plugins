---
name: workbench
description: >
  Create an interactive diagram or browser tool as a self-contained HTML bundle in a personal
  workbench server (~/workbench/tools/), where it auto-indexes on the home page and live-reloads.
  Trigger when the user asks for an interactive diagram, visualization, chart, dashboard,
  calculator, explorer, or any "tool I can open in a browser" — or says "add this to my workbench",
  "make a workbench tool", "put this on the workbench", or "/workbench".
  Use this instead of writing a one-off HTML file to a random path.
last_updated: 2026-06-05
created_by: Bear
---

# Workbench tool authoring

The workbench is a personal zero-dependency web server at `~/workbench/` (built on system `python3`).
It serves self-contained HTML/JS/CSS bundles from `~/workbench/tools/`, auto-generates a home page
that indexes them, and live-reloads any open tab when a file changes. Access it at
**http://localhost:8765**.

> **First time?** If `~/workbench/` doesn't exist yet, read
> `~/.claude/skills/workbench/SETUP.md` and run the setup before writing any tools.

## What to do when this triggers

1. **Pick a kebab-case name** for the tool (e.g. `sdlc-pipeline`, `pricing-explorer`).

2. **Choose single-file vs folder:**
   - **Single file** — `~/workbench/tools/<name>.html` with HTML, CSS, and JS all inline.
     This is the default. Ideal for diagrams and tools you can generate in one shot.
   - **Folder** — `~/workbench/tools/<name>/index.html` plus sibling `.js`/`.css`/asset files.
     Use only when the tool genuinely benefits from separate files (large datasets, several scripts).
     It still appears as one tool on the home page.

3. **Write the bundle** with the Write tool. Requirements:
   - Always include a meaningful `<title>` — the home page uses it as the tool's label.
   - Make it fully self-contained. CDN `<script>`/`<link>` tags (D3, Mermaid, Chart.js, etc.) are
     fine — the page renders in a local browser that has internet.
   - Do **not** add a live-reload script — the server injects one into every served `.html`
     automatically. Adding your own would double-fire.
   - Match the dark workbench aesthetic when reasonable (bg `#0f1116`, cards `#161922`,
     border `#262a36`, accent `#4c7dff`), unless the user asks for something else.

4. **Do not start or restart the server.** Just writing the file is enough — it appears on the home
   page and any open tab reloads within ~1s. (Only edits to `server.py` itself need a restart.)

5. **Tell the user the URL:** `http://localhost:8765/<name>.html`
   (or `http://localhost:8765/<name>/` for a folder tool). It's also linked from the home page
   at `http://localhost:8765/`.

## Notes

- Tools live ONLY in `~/workbench/tools/` — never in a shared folder or temp path.
- This is a personal scratch space for quick visuals and explorers, separate from formal deliverables.
