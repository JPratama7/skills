# Jujutsu commands

Load when the repo root has `.jj`. The working copy is itself a commit —
there is no staging step. Selectivity comes from splitting when unrelated
changes are mixed in.

```bash
jj describe -m "<message>"  # describe the current change
jj new                      # start the next change
jj split                    # split unrelated changes
```
