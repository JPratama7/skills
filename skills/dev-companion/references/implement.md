# `/dev-companion implement`

Act as the implementation specialist: make the smallest complete change that solves the request and fits the target repository. Apply `minimal-coding.md`, including the active lite/full/ultra level, before choosing the solution.

## Workflow

1. Read applicable `AGENTS.md` instructions. If style guidance is missing or incomplete, run `/dev-companion init` first, then return here.
2. Inspect the target code and trace the affected callers, tests, fixtures, configuration, and exports. For a bug, find callers of the affected function and fix the root cause in shared code where possible.
3. Reuse existing helpers and project patterns. Prefer the project's own components and conventions, then standard-library/platform features, then already-installed dependencies. Do not add dependencies, abstractions, options, or scaffolding nobody requested.
4. Implement the minimum clear solution. Finish all parts the task needs, and preserve existing validation/error handling when moving or merging code. Between similarly small choices, choose the one that handles edge cases correctly.
5. Add or update only the smallest useful checks for non-trivial behavior; trivial changes need no new test. Use the project's existing test tools.
6. Use TDD only when the user explicitly requests TDD, test-first development, red-green-refactor, or integration tests. In that case load `tdd.md` and follow the installed TDD skill. Otherwise implement first and run relevant checks.
7. Report what changed and checks run. State meaningful skipped scope or risks, not a generic checklist.

Never trade away input validation, security, accessibility, data safety, hardware calibration, or an explicit requirement for fewer lines.
