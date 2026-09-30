# Export format reference

`srs.py export <deck> --formats <list>` writes files into `<deck>/exports/`.
Canonical store is always `cards.jsonl`; exports are disposable — re-run after
any `add`.

## anki → `exports/anki.tsv`

Tab-separated, one card per line: `front<TAB>back<TAB>tags` (space-joined).
Newlines inside fields become `<br>`. Import: Anki → File → Import → pick the
file → map field 1→Front, 2→Back, 3→Tags.

Caveat: `qa` cards map to Basic notes. `cloze` cards keep `{{c1::…}}` in the
front field — to import them as real Cloze notes the user must select the
Cloze note type during import; if a deck mixes types, tell the user, or split
exports (`qa`→one file, `cloze`→another) when they ask for clean Anki cloze
imports.

## md → `exports/deck.md`

Human-readable rendering: `### <id>` heading per card with `**Q:**`/`**A:**`
lines; cloze shown with `{{c1::…}}` intact. For reading, diffing, pasting into
notes — not an app import format.

## obsidian → `exports/obsidian.md`

Matches the Obsidian *Spaced Repetition* plugin's multi-line format:

```
Question text
?
Answer text
```

Cards separated by blank lines. Cloze cards render with `==highlights==`
(plugin's cloze convention). The user picks the review tag/folder in plugin
settings; note that in your report.

## mochi → `exports/mochi.md`

Mochi's markdown import: `front\n---\nback` blocks separated by blank lines;
tags become `#tag` lines inside the back. Cloze deletions render as
`[...]text[...]` since plain markdown import doesn't carry occlusion — flag
this when a cloze-heavy deck goes to Mochi.

## Picking a format

- User named an app → export that format (+ `md` for preview)
- "Anki" → `anki`
- "Obsidian" → `obsidian`
- Unspecified → `md` + `anki`, mention alternatives
- In-chat review only → no export needed, but `md` is a nice artifact anyway
