# Integrate code

Loaded on demand — read when you are the member who integrates (the
`commits` role in the board's `ROLES` line).

One integration branch, one scripted pick loop. Write `.crew/pick.sh`
once — it applies a member's commits onto the integration branch — so
order and checks stay identical per pick.

## Order

1. **Baseline first.** Run the suite once on the base commit, in a
   separate worktree — never check out an old commit in the main tree.
   Record the failure list: that is the pre-existing set.
2. **Pick per member, in dependency order.** One member's batch at a
   time. Run the suite after every batch — never once at the end.
3. **Diff against baseline, not zero.** A batch is clean when its
   failure list equals the baseline's. "1 failure, the known one"
   approves by list, never by count.

## Expected conflicts

Shared registry files conflict by design:

- imports / mounts / registration lists → **keep both sides**;
- exclusion / not-yet-ported lists → **drop what a later pick already
  ported**;
- removals and modifications (not just adds) → resolve by intent: a
  mount one branch deleted stays deleted unless the removal was
  accidental — check the branch diff before re-adding.

## Post the head fast

The moment a batch verifies, mail the new head SHA to every lead so
they branch from it. Long merge gates land later as their own commit
on top — never hold a verified head while leads wait.

## Carry fixes down

Leads rebase long-lived branches (or carry the integration fix)
promptly. A failure already fixed upstream keeps firing downstream —
and the known-red noise masks the next real offence.
