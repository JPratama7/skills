#!/usr/bin/env bash
# Cherry-pick team commits onto the current branch of REPO_DIR, resolving the conflicts that parallel teams always
# cause, and stop on anything else.
#
#   pick.sh REPO_DIR SHA [SHA ...]
#
#   - A lockfile (LOCKFILE, default uv.lock): take ours, then run LOCK_CMD (default "uv lock -q"; never upgrade).
#     LOCK_CMD runs ONLY when the lockfile was actually conflicted — a failed pick with no lockfile conflict must
#     not rewrite lock state in this checkout.
#   - A pyproject.toml whose only conflicting change is a dependency or extras list: union by entry, keeping each
#     comment with its entry (resolve_pyproject.py). Any other pyproject change stops the run for a manual fix.
#   - A pick that becomes empty after resolving is skipped and reported.
#   - Git's own error is shown, never swallowed: a pick that fails with no conflicted files stops the run.
set -uo pipefail
REPO=${1:?usage: pick.sh REPO_DIR SHA...}; shift
LOCKFILE=${LOCKFILE:-uv.lock}; LOCK_CMD=${LOCK_CMD:-uv lock -q}
HERE=$(cd "$(dirname "$0")" && pwd)
cd "$REPO" || exit 1
for sha in "$@"; do
  if out=$(git cherry-pick "$sha" 2>&1); then echo "picked $sha"; continue; fi
  conflicts=$(git diff --name-only --diff-filter=U)
  if [ -z "$conflicts" ]; then
    if git rev-parse -q --verify CHERRY_PICK_HEAD >/dev/null && git diff --cached --quiet; then
      git cherry-pick --skip; echo "skipped $sha (empty)"; continue
    fi
    printf 'pick.sh: cherry-pick %s failed with no conflicted files:\n%s\n' "$sha" "$out" >&2
    exit 1
  fi
  lock_conflict=""
  for f in $conflicts; do
    case "$f" in
      "$LOCKFILE"|*/"$LOCKFILE") git checkout --ours -- "$f"; lock_conflict=1 ;;
      pyproject.toml|*/pyproject.toml) python3 "$HERE/resolve_pyproject.py" "$f" || { echo "RESOLVE BY HAND: $f in $sha"; exit 1; } ;;
      *) echo "RESOLVE BY HAND: $f in $sha"; exit 1 ;;
    esac
  done
  if [ -n "$lock_conflict" ]; then
    sh -c "$LOCK_CMD" || { echo "lock failed after $sha"; exit 1; }
  fi
  git add -A -- $conflicts
  [ -n "$lock_conflict" ] && git add -A -- "$LOCKFILE"
  if git diff --cached --quiet; then git cherry-pick --skip; echo "skipped $sha (empty after resolve)"; continue; fi
  if ! out=$(GIT_EDITOR=true git cherry-pick --continue 2>&1); then
    printf 'pick.sh: continue failed for %s:\n%s\n' "$sha" "$out" >&2
    exit 1
  fi
  echo "picked $sha (resolved)"
done
