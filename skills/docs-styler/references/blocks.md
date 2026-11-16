# Blocks

HTML + CSS patterns for common document blocks. Copy the CSS for each block
the document actually uses into the `<style>` block after the theme CSS.
Every rule is written against theme variables (`--accent`, `--border`, ...)
so blocks render correctly under all three themes without edits.

## Document header (`header.doc-header`)

Title + metadata line. Use when the source has a title, date, author,
status, or version.

```html
<header class="doc-header">
  <h1>Payment outage RCA</h1>
  <p class="doc-meta">2026-11-10 · A. Rivera · v1.2</p>
</header>
```

```css
.doc-header { margin-bottom: 2em; }
.doc-header h1 { margin-bottom: 0.15em; }
.doc-meta { color: var(--muted); font-size: 0.9em; margin: 0; }
```

## Table of contents (`nav.toc`)

Anchor-linked TOC for documents with 4+ sections. Every `href="#x"` must
have a matching `id="x"` — the validator fails on dead anchors. Hidden in
print by the shared print rules.

```html
<nav class="toc" aria-label="Table of contents">
  <h2>Contents</h2>
  <ol>
    <li><a href="#summary">Summary</a></li>
    <li><a href="#timeline">Timeline</a></li>
  </ol>
</nav>
```

```css
nav.toc {
  background: var(--accent-bg); border: 1px solid var(--border);
  border-radius: 6px; padding: 1em 1.4em; margin: 1.5em 0 2.5em;
}
nav.toc h2 { font-size: 0.95em; margin: 0 0 0.4em; text-transform: uppercase;
             letter-spacing: 0.05em; color: var(--muted); }
nav.toc ol, nav.toc ul { margin: 0; padding-left: 1.3em; }
nav.toc li { margin: 0.15em 0; }
```

## Callout / admonition (`aside.callout`)

For warnings, key facts, decisions. Types: `note` (default), `warning`,
`tip`, `important`. Label line is styled, not a real heading — callouts stay
out of the heading outline.

```html
<aside class="callout warning">
  <p class="callout-label">Warning</p>
  <p>Rollback requires the previous schema snapshot.</p>
</aside>
```

```css
aside.callout {
  border: 1px solid var(--border); border-left: 4px solid var(--accent);
  background: var(--accent-bg); border-radius: 6px;
  padding: 0.7em 1.1em; margin: 1.2em 0;
}
.callout-label {
  margin: 0 0 0.3em; font-weight: 600; font-size: 0.85em;
  text-transform: uppercase; letter-spacing: 0.04em; color: var(--accent);
}
.callout > :last-child { margin-bottom: 0; }
.callout.warning { border-left-color: #c58f00; }
.callout.warning .callout-label { color: #a17600; }
.callout.tip { border-left-color: #2e7d4f; }
.callout.tip .callout-label { color: #2e7d4f; }
.callout.important { border-left-color: #b0313a; }
.callout.important .callout-label { color: #b0313a; }
```

## Data table

Real `table` markup for tabular data. `th` for headers — never fake a table
with preformatted text.

```html
<table>
  <thead><tr><th>Service</th><th>Impact</th><th>Owner</th></tr></thead>
  <tbody>
    <tr><td>checkout</td><td>5xx errors</td><td>payments</td></tr>
  </tbody>
</table>
```

```css
table {
  border-collapse: collapse; width: 100%; margin: 1.2em 0;
  font-size: 0.95em;
}
th, td {
  text-align: left; padding: 0.45em 0.7em;
  border-bottom: 1px solid var(--border);
}
thead th {
  border-bottom: 2px solid var(--accent); font-weight: 600;
}
tbody tr:nth-child(even) { background: var(--accent-bg); }
```

## Figure (`figure`)

Use for images embedded as data URIs (rare — prefer describing the figure in
text) and for diagrams the source already contains as code (e.g. Mermaid —
keep it as a `pre` code block unless the user provides a renderer).

```html
<figure>
  <pre><code>graph TD; A-->B</code></pre>
  <figcaption>Request flow after the fix.</figcaption>
</figure>
```

```css
figure { margin: 1.4em 0; }
figcaption {
  color: var(--muted); font-size: 0.88em; margin-top: 0.5em;
  text-align: center;
}
```

## Code block

`pre > code`, always with a language class when known
(`class="language-sql"`) even though no highlighter ships — the class is
documentation and a hook for later.

```html
<pre><code class="language-sql">SELECT * FROM incidents;</code></pre>
```

Styled by the theme's `pre`/`code` rules — no extra CSS needed.

## Attention Conservation Notice (`.acn`)

doc-builder documents open with this block. Keep it near the top and style
it as a distinct panel — it must read as meta-information, not body prose.
Build it as a list, not four bare lines.

```html
<section class="acn" aria-label="Attention Conservation Notice">
  <h2>Attention Conservation Notice</h2>
  <ul>
    <li><strong>For:</strong> on-call engineers</li>
    <li><strong>What:</strong> payment outage on 2026-11-10</li>
    <li><strong>Action:</strong> review and approve</li>
    <li><strong>Skip if:</strong> you do not own payments</li>
  </ul>
</section>
```

```css
.acn {
  border: 1px solid var(--accent); border-radius: 6px;
  background: var(--accent-bg); padding: 0.8em 1.2em; margin: 1em 0 2em;
}
.acn h2 {
  font-size: 0.9em; margin: 0 0 0.4em; border: 0; padding: 0;
  text-transform: uppercase; letter-spacing: 0.05em; color: var(--accent);
}
.acn ul { margin: 0; padding-left: 0; list-style: none; }
.acn li { margin: 0.1em 0; }
```

## Choosing blocks

- Map source semantics to blocks: a "note/warning" sentence → `callout`;
  labelled intro metadata → `doc-header`; "For:/What:/Action:/Skip if:" →
  `.acn`; enumerated sections → `nav.toc`.
- Add a TOC only when the doc has 4+ sections — on short docs it is clutter.
- Do not invent blocks the source does not support (no fake summary cards).
