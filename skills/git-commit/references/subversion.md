# Subversion commands

Load when the repo root has `.svn`. Commits publish to the shared server
immediately — there is no local commit to inspect first, so the
confirmation step is not optional.

```bash
svn status                 # survey
svn diff                   # survey
svn add <paths>            # stage new files
svn commit -m "<message>"  # commit (immediate publish)
```
