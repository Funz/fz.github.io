# Caching Strategy

FZ caches results by the **MD5 hash of a case's input files**. A
[`cache://`](../calculators/cache.md) calculator reuses a previous result whenever the
input hashes match and the stored outputs are valid — no recomputation.

```title=".fz_hash"
a1b2c3d4e5f6...  input.txt
f6e5d4c3b2a1...  config.dat
```

Matching is by `.fz_hash` content, so it is independent of the
[`case_naming`](../core-functions/fzr.md#case-directory-naming-new-in-12) scheme used to
write the cache.

## Strategies

### Resume an interrupted run

```python
fz.fzr("input.txt", {"param": list(range(100))}, model,
       "sh://bash slow_calc.sh", results_dir="run1")
# interrupted with Ctrl+C after ~50 cases

fz.fzr("input.txt", {"param": list(range(100))}, model,
       ["cache://run1", "sh://bash slow_calc.sh"], results_dir="run1_resumed")
```

### Expand the parameter space

```python
fz.fzr("input.txt", {"temp": [100, 200, 300], "pressure": [1, 10, 100]}, model,
       "sh://bash calc.sh", results_dir="study1")           # 9 cases

fz.fzr("input.txt",
       {"temp": [100, 200, 300, 400, 500], "pressure": [1, 10, 100, 1000, 10000]},
       model, ["cache://study1", "sh://bash calc.sh"], results_dir="study2")  # reuses 9, runs 16
```

### Multi-tier cache

```python
calculators = [
    "cache://latest_run",
    "cache://archive/2024-*",
    "cache://archive/*/*",
    "sh://bash calc.sh",     # last resort
]
```

## What the Cache Keys On

Only the **input files**. It does **not** consider the calculator command, so:

- Changing the calculation script but not the inputs → still a cache hit.
- To force recomputation, run into a fresh `results_dir` with no `cache://` entry.

## `fzd` Caching

[`fzd`](../core-functions/fzd.md) adds two automatic layers on top:

- **Cross-iteration caching** — a point evaluated in one iteration is never re-run in a
  later one.
- **Re-run resume** — an existing `analysis_dir` is renamed with a timestamp and its
  iteration directories are added to the cache, so a re-run reuses all prior work.

## Housekeeping

```bash
# Drop result payloads older than 30 days but keep the cache keys
find results/ -type d -mtime +30 -exec rm -rf {} +
find results/ -type f ! -name '.fz_hash' -delete
```

## See Also

- [Cache Calculator](../calculators/cache.md) · [Interrupt Handling](interrupts.md) · [Parallel Execution](parallel.md)
- [`FZ_CACHE_DIR`](../../reference/environment.md#fz_cache_dir)
