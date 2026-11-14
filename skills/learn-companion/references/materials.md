# Material-grounded learning

The learner supplied their own materials — PDFs, slide decks, Word docs,
Markdown/TXT, webpage exports, pasted notes, OCR text — and wants to learn
from them. The materials define the scope; the attempt-first loop from
pedagogy.md still runs the teaching. Load [reliability.md](reliability.md)
alongside this file: generated content from materials cites sources, so
the grounding rules apply.

## The contract

- **Materials are the primary source.** Do not replace their content with
  generic domain knowledge. When material coverage and your own knowledge
  disagree, teach the material's version and flag the discrepancy.
- **Outside additions are marked `Supplemental`** wherever they appear —
  notes, quizzes, coverage maps. The learner must always be able to tell
  what came from their materials.
- **Never fabricate material content**: page numbers, slide numbers,
  chart contents, table values, figure structure, or topics not present.
  If you can't read it, you don't know it.
- **Unreadable or ambiguous content is logged, not guessed.** Record it
  in `issues.md` and either ask the learner or mark dependent content
  `Partially grounded`.

## Workspace

Material state lives under `.learn-companion/materials/` (persistent —
it grounds future sessions, so it is state, not scratch):

| File | Holds |
|---|---|
| `manifest.md` | One row per supplied item: name/path, format, extraction status (done / partial / unreadable) |
| `extracted/<name>.md` | Extracted text, OCR, table transcriptions, visual descriptions per source |
| `index.md` | Topic → location index (file + page/slide/section), visual markers for charts/diagrams/screenshots, and a coverage map linking roadmap topics to material locations |
| `issues.md` | Unresolved extraction problems and what was decided about each |

## Workflow

1. **Register** every supplied file, URL, and pasted block in
   `manifest.md` before extracting anything.
2. **Extract** to `extracted/` — text plus descriptions of charts,
   diagrams, screenshots a learner would need explained. Keep originals
   where they are; reference paths, don't copy.
3. **Index** in `index.md`: what topics exist, where they live, which
   elements are visual. The index is what later sessions read — they
   should not need to re-extract.
4. **Build from the index**: roadmap topics, explanations, and exercises
   ground to material locations first; mark gaps `Supplemental` or ask.
5. **Keep the coverage map current** as topics are added or mastered.

## No file-read fallback

If you cannot read the supplied files, say so — never claim to have read
them. Downgrade, in order: ask the learner to paste the relevant text;
ask for OCR or a Markdown/TXT export; produce only a material-processing
checklist they can run themselves. Then proceed with whatever they can
supply.
