# Harness comms maps

Loaded on demand — read when resolving the six primitives for your
harness (SKILL.md §6). `—` means the primitive doesn't exist there;
take the file fallback. The protocol never changes: append before
notify, subject not body, inbox-first on every wake. Only the
doorbell differs.

Resolution order is native tools first, herdr second: a harness's own
spawn/message tools beat pane commands where they exist. `HERDR_ENV=1`
only *suggests* herdr — verify it answers (`command -v herdr`, then a
cheap `herdr agent list`); the env var survives dead servers, and a
dead herdr means the file fallbacks, not dead commands.

## Herdr panes (`HERDR_ENV=1`)

| primitive | command |
|-----------|---------|
| `spawn`   | `herdr pane split --current --direction right --cwd "$PWD" --no-focus` → `.result.pane.pane_id`, then `herdr agent start <name> --kind <defaults.kind> --pane <id> -- --model <defaults.model>` |
| `notify`  | claude-kind: `SendMessage` to the member's session name (from `panes.txt`); other kinds / fallback: `herdr agent prompt <name> "<from> → <to>: <subject>"`. Never `send-keys`/`send-text` into a pane a person uses |
| `tail`    | `herdr agent read <name> --source recent-unwrapped --lines 120` |
| `wait`    | `herdr agent wait <name> --until idle --until done --timeout <ms>` — repeat `--until` per state; a member already `done` misses an idle-only wait. Check the output for an `error` key: failures return as JSON, not exit codes |
| `probe`   | `herdr agent get <name>` / `herdr agent list` |
| `signal`  | `herdr notification show "<title>" --body "<text>"` |

- Herdr names survive restarts — they ARE the stable identity for
  `agent prompt`/`agent wait`. But `SendMessage` addresses claude
  sessions by session name, so a SendMessage crew still keeps
  `panes.txt` — mapping each member to its session (root first,
  builders from worktree-named sessions, the rest register at boot;
  SKILL.md §6).
- `agent prompt --wait` doubles as dispatch-confirm: it fails
  `agent_prompt_stalled` when no activity follows submission, and
  `agent_blocked` when a permission dialog holds the pane.
- A prompt into a `blocked` agent is rejected before any bytes send —
  the approval UI is the user's to answer. Never `send-keys` around
  another session's prompt.
- Pane agents can spawn — sub-leads start their own teammates. Keep
  agent panes ≤4 per tab; a fifth opens a second tab.
- herdr can exit 0 on bad arguments and prints usage instead of
  failing — check the JSON result (`"changed":true`, an `error` key),
  never the exit code.
- Regrouping panes: `herdr pane move <id> --tab <tab_id> --target-pane
  <id> [--split right|down]` — `--target-pane` requires `--tab`. A
  lead-plus-builders layout: lead pane left, builders moved right then
  split down.

## Devin builtin (`run_subagent`)

| primitive | mechanism |
|-----------|-----------|
| `spawn`   | `run_subagent` `is_background: true` → returns `agent_id` |
| `notify`  | `run_subagent` `resume: <agent_id>` — **foreground only**: it blocks you. Append mail as it arrives; resume once per batch with "check inbox". |
| `tail`    | `read_subagent <agent_id>` |
| `wait`    | passive — the completion notification arrives on its own; integrate then |
| `probe`   | `read_subagent` status fields |
| `signal`  | your normal reply — no out-of-band channel exists |

- Members can't spawn by default (nesting off) → sub-leads need a
  custom profile with `max-nesting`, or run the crew on herdr instead.
- No member→member channel — the lead relays every cross-member mail.
  DISPATCH stays file-based and still works.
- `notify`-blocks-the-lead reshapes cadence: don't ping per message.
  The inbox file absorbs bursts; one resume delivers the batch.
- Record each `agent_id` in `status` at spawn — it is the member's
  channel address and dies with the session (rebuild via `panes.txt`).

## File-only

No agent channel: a plain terminal, a harness with no re-prompt, a
member that can't be woken.

- `notify` / `wait` / `probe` → —. The stall-check is the whole loop;
  leads poll inboxes and relay on their next contact with each member.
- `tail` → last report file, handoff note.
- `signal` → your reply.
- Members compensate with discipline: inbox on every wake, handoff
  file current, reports mailed even mid-task — silence reads as a
  stall on this harness.
