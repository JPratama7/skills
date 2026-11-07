# Harness comms maps

Loaded on demand — read when resolving the six primitives for your
harness (SKILL.md §6). `—` means the primitive doesn't exist there;
take the file fallback. The protocol never changes: append before
notify, subject not body, inbox-first on every wake. Only the
doorbell differs.

## Herdr panes (`HERDR_ENV=1`)

| primitive | command |
|-----------|---------|
| `spawn`   | `herdr pane split --current --direction right --cwd "$PWD" --no-focus` → `.result.pane.pane_id`, then `herdr agent start <name> --kind devin --pane <id> -- --model <defaults.model>` |
| `notify`  | `herdr agent prompt <name> "mail <from>: <subject>"` |
| `tail`    | `herdr agent read <name> --source recent-unwrapped --lines 120` |
| `wait`    | `herdr agent wait <name> --until <idle\|working\|blocked\|done> --timeout <ms>` |
| `probe`   | `herdr agent get <name>` / `herdr agent list` |
| `signal`  | `herdr notification show "<title>" --body "<text>"` |

- Herdr names survive restarts — they ARE the stable identity; this
  harness doesn't need `panes.txt`.
- `agent prompt --wait` doubles as dispatch-confirm: it fails
  `agent_prompt_stalled` when no activity follows submission, and
  `agent_blocked` when a permission dialog holds the pane.
- A prompt into a `blocked` agent is rejected before any bytes send —
  the approval UI is the user's to answer. Never `send-keys` around
  another session's prompt.
- Pane agents can spawn — sub-leads start their own teammates. Keep
  agent panes ≤4 per tab; a fifth opens a second tab.

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
