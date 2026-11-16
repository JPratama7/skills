# Themes

A theme is a complete CSS spec. Copy the chosen theme's CSS verbatim into the
document's single `<style>` block, then append the block CSS for every block
the document uses (`blocks.md`) and the shared print rules below. Adjust look
only through the CSS variables (`--bg`, `--fg`, `--accent`, ...) — block CSS
is written against those variables so all three themes stay consistent.

## Document skeleton

Every output file starts from this shape:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DOCUMENT TITLE</title>
<style>
/* theme CSS (verbatim) */
/* block CSS for blocks used */
/* shared print rules */
</style>
</head>
<body>
<main class="doc">
  <!-- semantic content -->
</main>
</body>
</html>
```

- `<title>` is the document's real title, never "Document" or left empty.
- `lang` matches the document's language.
- All content lives in `main.doc`. Optional `header.doc-header` and
  `nav.toc` go inside `main` before the first section.

## Picking a theme

| Theme | Use when |
|-------|----------|
| `default` | Anything unspecified; light report look for screen and print |
| `dark` | "dark mode", screen-first reading, dashboards-flavored docs |
| `compact` | "for printing", "handout", "dense", long docs meant to be read on paper |

Absent a request → `default`. A `.memory/memory.json` `docs-styler` entry can
set a different standing default.

## Shared print rules (append to every theme)

Print always produces a light, ink-friendly page regardless of screen theme.
Copy this block verbatim at the end of every stylesheet:

```css
@media print {
  :root { --bg: #ffffff; --fg: #1a1a1a; --muted: #444444;
          --accent: #1a4fa0; --accent-bg: #f0f4fa; --border: #cccccc;
          --code-bg: #f5f5f5; }
  body { background: #ffffff; font-size: 11pt; }
  .doc { max-width: none; padding: 0; }
  nav.toc, .no-print { display: none; }
  a { color: inherit; text-decoration: none; }
  h1, h2, h3, h4 { page-break-after: avoid; }
  table, figure, pre, aside.callout, .acn { page-break-inside: avoid; }
  pre { white-space: pre-wrap; word-wrap: break-word; }
}
```

Notes:
- `--accent` in print stays a dark blue so headings keep hierarchy on paper;
  it is not the screen accent when that would print too light.
- `nav.toc` hides in print — a printed TOC with dead links is noise. Keep it
  on screen.
- `pre` wraps in print so code does not clip off the page.

## Theme: default

Clean light report. System sans for UI feel, high legibility on screen.

```css
:root {
  --bg: #ffffff;      --fg: #1c1e21;      --muted: #5f6368;
  --accent: #1a4fa0;  --accent-bg: #eef3fb; --border: #d9dce0;
  --code-bg: #f4f5f7; --measure: 70ch;
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font: 1rem/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
        "Helvetica Neue", Arial, sans-serif;
}
.doc { max-width: var(--measure); margin: 0 auto; padding: 3rem 1.25rem; }
h1, h2, h3, h4 { line-height: 1.25; color: var(--fg); margin: 2em 0 0.6em; }
h1 { font-size: 1.9rem; margin-top: 0; border-bottom: 2px solid var(--accent);
     padding-bottom: 0.3em; }
h2 { font-size: 1.4rem; }
h3 { font-size: 1.15rem; }
p { margin: 0.7em 0; }
a { color: var(--accent); }
ul, ol { padding-left: 1.4em; }
li { margin: 0.3em 0; }
strong { color: var(--fg); }
hr { border: 0; border-top: 1px solid var(--border); margin: 2.5em 0; }
blockquote {
  margin: 1em 0; padding: 0.4em 1em; color: var(--muted);
  border-left: 3px solid var(--border);
}
code {
  font: 0.875em/1.5 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  background: var(--code-bg); padding: 0.15em 0.35em; border-radius: 3px;
}
pre {
  background: var(--code-bg); border: 1px solid var(--border);
  border-radius: 6px; padding: 0.9em 1.1em; overflow-x: auto;
}
pre code { background: none; padding: 0; }
```

## Theme: dark

Screen-first dark reading. Prints light — the shared print rules handle it.

```css
:root {
  --bg: #14161a;      --fg: #e4e6ea;      --muted: #9aa0a8;
  --accent: #7aa8f0;  --accent-bg: #1e2530; --border: #33383f;
  --code-bg: #1c2027; --measure: 74ch;
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font: 1rem/1.7 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
        "Helvetica Neue", Arial, sans-serif;
}
.doc { max-width: var(--measure); margin: 0 auto; padding: 3rem 1.25rem; }
h1, h2, h3, h4 { line-height: 1.25; color: #f0f2f5; margin: 2em 0 0.6em; }
h1 { font-size: 1.9rem; margin-top: 0; border-bottom: 2px solid var(--accent);
     padding-bottom: 0.3em; }
h2 { font-size: 1.4rem; }
h3 { font-size: 1.15rem; }
p { margin: 0.7em 0; }
a { color: var(--accent); }
ul, ol { padding-left: 1.4em; }
li { margin: 0.3em 0; }
hr { border: 0; border-top: 1px solid var(--border); margin: 2.5em 0; }
blockquote {
  margin: 1em 0; padding: 0.4em 1em; color: var(--muted);
  border-left: 3px solid var(--border);
}
code {
  font: 0.875em/1.5 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  background: var(--code-bg); padding: 0.15em 0.35em; border-radius: 3px;
}
pre {
  background: var(--code-bg); border: 1px solid var(--border);
  border-radius: 6px; padding: 0.9em 1.1em; overflow-x: auto;
}
pre code { background: none; padding: 0; }
```

Dark notes: keep contrast muted (off-white text, not pure `#fff`; accent is
desaturated). Do not add `prefers-color-scheme` — dark is chosen, not
detected.

## Theme: compact

Dense report for print-first handouts. Slightly smaller type, tighter
spacing, hairline rules — still comfortable on screen.

```css
:root {
  --bg: #ffffff;      --fg: #1c1e21;      --muted: #5f6368;
  --accent: #1a4fa0;  --accent-bg: #eef3fb; --border: #d9dce0;
  --code-bg: #f4f5f7; --measure: 76ch;
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font: 0.925rem/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
        "Helvetica Neue", Arial, sans-serif;
}
.doc { max-width: var(--measure); margin: 0 auto; padding: 2rem 1rem; }
h1, h2, h3, h4 { line-height: 1.25; color: var(--fg); margin: 1.4em 0 0.4em; }
h1 { font-size: 1.55rem; margin-top: 0; border-bottom: 2px solid var(--accent);
     padding-bottom: 0.25em; }
h2 { font-size: 1.2rem; }
h3 { font-size: 1.02rem; }
p { margin: 0.45em 0; }
a { color: var(--accent); }
ul, ol { padding-left: 1.3em; }
li { margin: 0.15em 0; }
hr { border: 0; border-top: 1px solid var(--border); margin: 1.6em 0; }
blockquote {
  margin: 0.8em 0; padding: 0.3em 0.9em; color: var(--muted);
  border-left: 3px solid var(--border);
}
code {
  font: 0.85em/1.45 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  background: var(--code-bg); padding: 0.1em 0.3em; border-radius: 3px;
}
pre {
  background: var(--code-bg); border: 1px solid var(--border);
  border-radius: 5px; padding: 0.7em 0.9em; overflow-x: auto;
}
pre code { background: none; padding: 0; }
```
