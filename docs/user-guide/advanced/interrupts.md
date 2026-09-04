# Interrupt Handling

`fzr` and `fzd` install a `SIGINT` handler so **Ctrl+C** stops a run cleanly instead of
leaving orphaned processes or half-written directories.

## What Happens on Ctrl+C

```
⚠️  Interrupt received (Ctrl+C). Gracefully shutting down...
```

1. Cases already running are allowed to finish.
2. No new cases are started.
3. Results collected so far are written out.
4. For `ssh://` / `slurm://` / `funz://`, the remote job is signalled to terminate and
   the remote temp directory is cleaned up.

A second Ctrl+C forces an immediate exit.

## Resuming

Because completed cases are on disk with their `.fz_hash`, add a
[`cache://`](../calculators/cache.md) entry pointing at the interrupted run:

```python
try:
    fz.fzr("input.txt", variables, model, "sh://bash calc.sh", results_dir="run1")
except KeyboardInterrupt:
    print("Interrupted — partial results saved")

fz.fzr("input.txt", variables, model,
       ["cache://run1", "sh://bash calc.sh"], results_dir="run1_resumed")
```

## Calling From a Background Thread (1.2)

Signal handlers can only be installed from the main thread. Since **1.2**, `fzr` / `fzd`
detect when they are called off the main thread (Streamlit reruns, a
`ThreadPoolExecutor` worker, an app embedding fz) and **skip** the handler install
instead of raising `ValueError: signal only works in main thread`. Ctrl+C handling is
simply unavailable in that case; everything else works normally.

## See Also

- [Caching Strategy](caching.md) · [Cache Calculator](../calculators/cache.md)
- [Parallel Execution](parallel.md)
