---
name: docs-styler
version: 1.0.0
description: Turn an existing document into a styled, self-contained HTML
  page — reports, notes, RCAs, changelogs, proposals, any written doc.
  Use whenever the user asks for a "styled HTML version", "web page
  version", "printable HTML", "render this markdown/doc as HTML", "export
  this report as a web page", or "make this doc look good" — including
  output produced by doc-builder or any other markdown/text source.
  Not for building apps, sites, or UI components.
---

# docs-styler

Style existing content into one polished `.html` file that reads well on
screen and prints cleanly. This skill is a presentation layer: it shapes how
a document looks, never what it says.

## Workflow

1. **Get the source** — a file path, pasted content, or output from another
   skill. If there is no source and none is implied by context, ask for it.
   Read the whole source before styling; partial reads produce dropped
   sections.
2. **Pick a theme** — `references/themes.md` defines the named themes
   (`default`, `dark`, `compact`) as complete CSS specs. Match an explicit
   request ("dark version", "for printing", "dense handout") to a theme;
   otherwise use `default`. One theme per document — never blend.
3. **Restructure into semantic HTML** — reorganize for readability
   (headings, lists, callouts, tables) while preserving every fact, number,
   decision, and name from the source. Fidelity rules below.
4. **Write the full `.html` file** — the complete document: doctype, head
   with meta and one inlined `<style>` block, semantic body markup. Assemble
   the stylesheet from the chosen theme's CSS plus the block CSS for every
   block used (`references/blocks.md`). Copy theme/block CSS verbatim and
   only adjust via the theme's CSS variables — do not freewheel new colors,
   fonts, or spacing outside the tokens.
5. **Validate** — run `python3 <skill-dir>/scripts/check_html.py <file>.html`
   and fix every reported problem before delivery. The check is the contract
   for "self-contained and print-ready"; a document that fails it is not
   done.
6. **Deliver** — save beside the source as `<source-name>.html` unless the
   user names a location. Report the path and the theme used.

## Fidelity rules

The skill restyles content; it does not author it.

- Preserve all substance: facts, figures, dates, names, decisions, caveats.
  Reorder and reformat freely; drop nothing decision-bearing.
- Never invent content to fill a gap — no placeholder lorem ipsum, no made-up
  metrics or attributions. Genuinely missing material becomes a visible
  `TODO:` line describing what is needed.
- Section order may change only when the source has no required order. Docs
  from doc-builder (RCA, report, requirements, decision record) keep their
  section order — downstream readers rely on it. An `Attention Conservation
  Notice` block stays near the top; style it with the `.acn` block, do not
  remove it.

## Rules

- One file, fully self-contained: all CSS inside a single `<style>` element
  in `<head>`; no `<link>` stylesheets, no external fonts, images, scripts,
  or CDN URLs; no `@import` and no `url(...)` pointing outside the file.
- No JavaScript. Documents ship without `<script>` — if the user asks for
  interactivity, flag it as out of scope rather than adding scripts.
- Always include `@media print` rules (the theme specs ship them): white
  background, dark text, sane page breaks. Print output never depends on the
  screen theme — a `dark` doc prints light.
- Screen output respects the theme as written: responsive measure, generous
  line-height, no auto `prefers-color-scheme` switching — theme choice is
  explicit so the file renders identically for every reader.
- Semantic HTML only: `main`, `header`, `nav`, `section`, `article`,
  `figure`/`figcaption`, real `table` markup, ordered heading hierarchy.
  Styling hooks are classes from `references/blocks.md`, not `div` soup.
- Every in-page link (`href="#id"`) resolves to an existing `id` — the
  validator enforces this; a TOC with dead anchors is worse than no TOC.
- Keep the document's voice and person. Restyling an "I deployed" RCA into
  third person changes the account, not just the look.

## Memory

`.memory/memory.json` → `docs-styler`: default theme and default output
directory, if the user names them. A stored default theme applies when the
request does not specify one.

## Bundled scripts

- `scripts/check_html.py <file.html>` — validates the delivery contract:
  single `<style>` with real CSS, zero external references, `@media print`
  present, `<title>`/`lang`/viewport/charset present, no `<script>`, every
  `href="#..."` resolves. Exit 0 clean, exit 1 with one line per problem.

## Reference files (load on demand)

- Picking or applying a theme, the document skeleton, shared print rules →
  `references/themes.md`
- Callouts, TOC, tables, figures, code blocks, doc headers, ACN styling →
  `references/blocks.md`
