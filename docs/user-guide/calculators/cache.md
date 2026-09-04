# Cache Calculator (`cache://`)

The `cache://` calculator does not run anything. It looks in one or more existing result
directories for a case whose **input files hash identically** to the current case and,
if it finds one with valid outputs, copies those results in — skipping the computation.

Put it **first** in a calculator list so real calculators only run on cache misses.

## URI Syntax

```
cache://path/to/results
```

```python
calculators = "cache://previous_run"

calculators = ["cache://run1", "cache://archive/results"]      # several caches

calculators = ["cache://archive/2024-*/results"]               # glob patterns

calculators = [
    "cache://previous_results",   # try cache first
    "sh://bash calculate.sh",     # compute on miss
]
```

## How It Works

1. Compute the MD5 hash of every input file for the current case.
2. Search the cache directories for a `.fz_hash` file whose entries all match.
3. Check that the cached outputs are non-`None`.
4. On a hit, copy the cached result files in and mark the case `done`; on a miss, fall
   through to the next calculator.

Matching is by `.fz_hash` **content**, not directory name — so a cache written with any
[`case_naming`](../core-functions/fzr.md#case-directory-naming-new-in-12) scheme
(`path` / `hash` / `index`) still matches.

```title=".fz_hash"
a1b2c3d4e5f6...  input.txt
f6e5d4c3b2a1...  config.dat
```

!!! note
    The cache keys on **input files only**, not on the calculator command. Editing your
    calculation script but not the inputs will still produce a cache hit — use a fresh
    `results_dir` without `cache://` to force recomputation.

## Common Uses

=== "Resume an interrupted run"

    ```python
    fz.fzr("input.txt", {"p": range(100)}, model, "sh://bash calc.sh", "run1")
    # ... Ctrl+C after 50 cases ...
    fz.fzr("input.txt", {"p": range(100)}, model,
           ["cache://run1", "sh://bash calc.sh"], "run1_resumed")
    ```

=== "Expand the parameter space"

    ```python
    fz.fzr("input.txt", {"t": [100, 200, 300]}, model, "sh://bash calc.sh", "study1")
    fz.fzr("input.txt", {"t": [100, 200, 300, 400, 500]}, model,
           ["cache://study1", "sh://bash calc.sh"], "study2")   # reuses 3, runs 2
    ```

=== "Multi-tier cache"

    ```python
    calculators = [
        "cache://latest_run",
        "cache://archive/2024-*",
        "cache://archive/*/*",
        "sh://bash calc.sh",
    ]
    ```

## See Also

- [Caching Strategy](../advanced/caching.md) — deeper patterns
- [Interrupt Handling](../advanced/interrupts.md)
- [`fzd` cross-iteration caching](../core-functions/fzd.md#cross-iteration-caching)
