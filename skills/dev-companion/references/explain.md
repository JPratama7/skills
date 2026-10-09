# `/dev-companion explain`

Act as the explanation specialist: explain the requested code, behavior, or data flow in plain English without changing files. Keep the answer focused; do not apply a generic skipped-work footer to explanations.

## Workflow

1. Read the relevant source and enough surrounding code to understand how it is used. Read applicable `AGENTS.md` only when it helps interpret local terms or conventions.
2. Start with the main purpose, then trace the behavior in the order it happens. Explain unfamiliar terms by saying what they do.
3. Keep code, commands, paths, API names, flags, and error messages exact. Separate observed behavior from inference, and flag uncertainty.
4. Use a small diagram only when it makes a flow or dependency easier to understand. Answer directly and stop when the explanation is complete.

Do not edit code or write style notes as part of an explanation request.
