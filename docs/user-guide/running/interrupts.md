# Interrupt & Resume

## Ctrl+C during `fzr` / `fzd`

| | Effect |
|--|--------|
| First Ctrl+C | No new case starts. Running local processes are terminated (killed after 5 s); remote and SLURM jobs are cancelled and remote temporary directories cleaned. Interrupted cases get `status="interrupted"`. `fzr` **returns** the DataFrame; the manifest records the interruption |
| Second Ctrl+C | `KeyboardInterrupt` is raised immediately |

So a script usually does not need `try/except KeyboardInterrupt`: after the first
Ctrl+C the call returns normally with partial results.

```python
results = fz.fzr("input.txt", variables, model,
                 calculators="sh://bash calc.sh", results_dir="run1")
print(results["status"].value_counts())     # done / interrupted
```

## Resuming

Completed cases are on disk with their `.fz_hash`. Run again with a cache entry:

```python
# in place: cache://_ = previous content of results_dir (renamed with a timestamp)
fz.fzr("input.txt", variables, model,
       calculators=["cache://_", "sh://bash calc.sh"], results_dir="run1")

# or into a new directory
fz.fzr("input.txt", variables, model,
       calculators=["cache://run1", "sh://bash calc.sh"], results_dir="run1_resumed")
```

Interrupted cases have no valid outputs, so they are recomputed.

## Calls from a non-main thread

Python only allows signal handlers in the main thread. When `fzr`/`fzd` run in another
thread (Streamlit, a thread pool, a web server), fz skips the handler: everything works
except the graceful Ctrl+C handling.

## See also

[Caching](caching.md) · [Cache calculator](../calculators/cache.md)
