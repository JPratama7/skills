# Git commands

Load when the repo root has `.git`.

## Survey

```bash
git status                 # what's modified, staged, untracked
git diff                   # unstaged changes
git diff --staged          # staged changes
git log --oneline -10      # recent history = commit message convention
```

## Stage deliberately

```bash
git add <path>             # stage by path, one logical change
git add -p <path>          # interactive hunk staging — file mixes task + unrelated edits
```

## Commit and verify

Heredoc keeps quoting and multi-line bodies intact:

```bash
git commit -m "$(cat <<'EOF'
fix(auth): refresh tokens before expiry

Why this is needed...
EOF
)"
git status                 # confirm nothing unexpected remains
git log -1 --stat          # confirm exactly what landed
```
