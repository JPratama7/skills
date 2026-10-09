# Minimal coding

Use for `/dev-companion implement` and `/dev-companion review`. Goal: solve the whole request with the least clear code. Be lazy about code, never about understanding, completion, or safety.

## Procedure

1. **Scope.** Read the request and relevant code. Trace callers, tests, fixtures, config, exports, and affected data. Check what could break, expose, or destroy. Do not add unrelated work.
2. **Question scope.** Skip features, options, and flexibility not requested or justified. For a vague build request, deliver the smallest useful core. In `ultra`, challenge each requested part before building; still deliver the justified core. In `lite`, do the task and mention a smaller viable option for the person to choose.
3. **Choose the first working option.** Reuse the project's helper, component, dependency, and conventions. Otherwise prefer standard library or platform features, then installed dependencies. Add no dependency for a few lines. Use one line only if it is clear at a glance; otherwise use the minimum readable code.
4. **Complete the change.** Update every affected caller, test, fixture, and config. Fix bugs at the shared root after checking callers, not with repeated caller guards. Keep the project's layers and interfaces. Avoid unrequested abstractions, wrappers, conversions, options, config, boilerplate, and "for later" code. Prefer deletion. A diff that needs decoding is not simple.
5. **Preserve correctness.** Keep edge-case handling. Translate words like *inclusive*, *exclusive*, and *at least* into exact boundaries, then check both boundary values. When moving or merging code, keep its validation and error handling. Never cut trust-boundary validation, data-loss protection, security, accessibility, hardware calibration, or explicit requirements.
6. **Comment and check.** Do not comment obvious code. Add one concise comment only for a why the code cannot show. For a known shortcut limit, write `shortcut: <limit>, <when to upgrade>`. New non-trivial logic gets one small test or assert-based self-check that covers its main case and key failure/boundary case; trivial changes need none. TDD is opt-in: test first only when explicitly requested; otherwise implement, then run relevant checks.
7. **Report.** Give the result, then one or two short lines on meaningful omissions, unchecked items, or risks. Do not invent caveats. Do not claim inspection, searches, or checks you did not perform; reason from supplied code when it is sufficient. `/dev-companion explain` has no generic footer.

## Ambiguity

If a safe default exists, state it and proceed. If a missing requirement changes correctness or safety and has no safe default, ask one focused question. For a large request, deliver the smallest useful slice and name what remains; do not silently drop requirements.

## Level persistence

Default is `full`. `/dev-companion lite|full|ultra` sets the level for the session. It remains active until another level, `/dev-companion stop`, or `/dev-companion normal`. Apply it to implementation and review; a level never overrides safety or explicit requirements.

- `lite`: fulfill the request; mention a smaller viable option and let the person choose.
- `full`: follow the procedure above.
- `ultra`: challenge unsupported scope before building the justified core.

## Output pattern

`[change]. Skipped: [unneeded scope]. Check/risk: [material item, if any].`
Use only the parts that apply.