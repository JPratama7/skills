# `/learn-companion study`

The core tutoring session. Read [pedagogy.md](pedagogy.md) first — the
attempt-first loop below only works if you follow it.

## Workflow

1. Read `.learn-companion/` state. Resolve any `## Pending decision` in
   `progress.md` first — a pending attempt or advance choice is mid-loop,
   not optional. Then check `## Review due` items; if today's session was
   meant for new material, due items can fold into warmup or defer to
   `/learn-companion review` — ask, don't silently skip.
2. Pick the topic: the learner's request, or the next unmastered topic on
   the roadmap. One topic at a time; breadth sessions dilute retrieval.
3. Probe prior knowledge with one retrieval question — "what do you
   already know about X" or a small prediction — before teaching. This
   isn't a quiz wall; one question calibrates where to start.
4. Teach what's unfamiliar: direct, clear explanation using Concept and
   Why this matters callouts where they help. Unguided discovery fails
   novices — don't make them derive what they can't yet see.
5. Attempt: the learner applies the concept — a problem, prediction,
   example of their own, or explanation in their own words — committed
   before any feedback. For complex multi-step material, scaffold:
   worked example → completion problem → independent problem → retrieval.
6. Feedback on their actual reasoning, then Mastery check: by default a
   teach-back pass — the learner explains the topic end-to-end in their
   own words while you probe gaps one at a time (spec in pedagogy.md).
   Confirm the error is corrected or the idea re-derived before
   advancing. Mark the topic mastered only on a teach-back that
   survives with no failure tells, and update `progress.md`,
   `roadmap.md`, and the topic's review schedule.
7. Before ending a turn that awaits a learner reply, write the
   `## Pending decision` section in `progress.md` — what was asked and
   what answer is awaited — per pedagogy.md's evidence rules. Then end
   with a Session report: covered, demonstrated, shaky, next review
   date.

Respect explicit requests to just get an explanation — give it, note the
skipped attempt, and continue. Ordinary "keep going" retains the loop.

## Teacher side — building class materials

Routes here: lesson plans, lecture notes, slide outlines, in-class
activities, teaching cases, discussion guides, flipped packages, rendered
decks, STEM labs, recorded-video scripts, bilingual versions. Checkpoints
use the teacher-side block in pedagogy.md. A lesson serves the week's
outcomes — material mapped to no outcome gets flagged once (§2), then the
professor decides; never silently built or silently dropped.

### Lesson package (one class meeting)

1. LOAD — the week's topic, outcomes, assessments due, learner profile,
   class size, modality, length (from the passport, or ask standalone).
2. ARC — opener → timed segments → at least one active segment per 20–25
   min (§4), scaled to size/modality → closure → contingency notes.
   🧑 checkpoint: the cheapest moment to change the lesson's shape.
3. BUILD — lecture notes (signal-before-detail, worked examples,
   anticipated misconceptions, `[VERIFY]` on uncertain claims), slide
   outline (one idea per slide, assertion titles, figure specs with alt-text
   notes), activity sheets — all against the same confirmed arc.
4. ASSEMBLE — package from `assets/lesson-builder/templates/`; cross-check
   timings agree; collect every `[VERIFY]` into one review list.
   🧑 checkpoint → passport week updated (append-only, post-confirmation).

Activities are runnable, not aspirational: timing, group size, materials,
the launch script (what the instructor literally says), failure modes with
fixes. Modes: single artifacts (lecture-notes, slides-outline, activities,
case-study, discussion-guide, flipped — pre-class spec + in-class
application session) or week-batch per the pipeline's chosen depth. Depth
refs: `assets/lesson-builder/references/lesson_anatomy.md`,
`active_learning_catalog.md`.

### Rendered decks

The markdown/spec source is the deck of record; PDF/PPTX/HTML are rebuild
products. **Never fake a render** — no working toolchain → ship the source,
the exact install command, and what the build would produce. Detect what's
installed (marp / pandoc / tectonic / python-pptx) and report plainly.
Course theme spec once (`assets/deck-studio/templates/theme_spec_template.md`),
every deck against it. Figures are code — generating script stored beside
the image, colorblind-safe, alt-texted. Accessibility floor enforced:
24pt body minimum, contrast-checked pairs, alt text per figure — violations
flagged with slide numbers, professor may override with a logged reason.
The deck adds zero new domain claims; inherited `[VERIFY]` markers survive.
Rulebook: `assets/deck-studio/references/slide_design_rules.md`;
toolchains: `toolchain_guide.md` (degradation ladder).

### STEM labs (executable artifacts)

Everything ships **executed, not assumed** — the scaffold runs as shipped,
the dataset's planted effect is recovered by the intended analysis, the
reference solution was solved cold from student-facing materials only, the
autograder passes the solution and scores ~0 on the bare starter. The
verification record (commands, outputs, dates) ships with the package;
what couldn't be executed carries `[VERIFY]`. Ground truth (seeds, planted
effects, expected values, seed↔student map) lives in a professor-only file —
it never leaks into test names, feedback strings, or error messages.
Per-student variants ship with an equivalence argument (same concepts,
method, step count, difficulty class) and a spot-solve sample. Dependencies
pinned; the README's fresh-env instructions were followed cold. Synthetic
data is labeled synthetic wherever realism could mislead; real datasets
need professor-supplied provenance and license. Patterns:
`assets/lab-forge/references/synthetic_data_patterns.md`,
`autograder_patterns.md`; handout: `templates/lab_handout_template.md`.

### Recorded media (scripts, storyboards, captions)

Scripts are spoken register — short sentences, direct address; the
read-aloud test is part of the draft pass. Default 6–9 min per episode
(`assets/media-scripter/references/video_pedagogy.md` for the honest
evidence scope), one objective and ≥1 embedded retrieval prompt each;
longer only with a logged reason. Two-column format (narration + visual
cues, ~130–150 wpm): every visual change has a narration anchor, every
narration reference names its visual — orphans are defects. "This graph"
is banned; say what it shows. Captions are planned from the start — a
script ships with its transcript. New examples invented for recording are
marked for vetting; `[VERIFY]` on uncertain claims. Modes: script |
storyboard | series | captions | audio.
Templates: `assets/media-scripter/templates/`.

### Bilingual courseware

**Glossary-first** — no term-bearing translation without a
professor-confirmed glossary covering its terms; new terms mid-translation
pause for confirmation rather than being improvised. Pedagogical
equivalence over literalism: the translated artifact makes the same
pedagogical demand; deliberate divergences are logged with location and
reason, and assessment translations are checked for difficulty shift (an
exam harder in one language is an equity defect). Version pairing is
recorded — what matches what at which version; drift reports loudly.
Read-only consistency audits locate every finding, no silent rewrites.
Conventions: `assets/bilingual-courseware/references/emi_conventions.md`;
templates: `assets/bilingual-courseware/templates/`.
