# Cache (`cache://`)

`cache://` runs nothing. For each case it looks in previous result directories for a
case with the **same input hash** (and compatible code identity) whose outputs are all
valid, and copies its results. On a miss, the next calculator in the list runs the case.

```text
cache://path          # a results directory, or a glob
```

```python
calculators = ["cache://run1", "sh://bash calc.sh"]                  # reuse, else compute
calculators = ["cache://run1", "cache://archive/2024-*", "sh://bash calc.sh"]
```

Put `cache://` entries **first**. They do not count as parallel workers.

## Matching rules

1. The case's `.fz_hash` — SHA-256 of every compiled input file and of the
   `input_static` files — must equal a cached case's `.fz_hash`.
2. Code identity: if both calculators declare a `code_id`, they must be equal; if the
   identity cannot be verified (no `code_id`), the match is accepted with a one-time
   warning, or refused with `FZ_CACHE_STRICT=1`.
3. The cached outputs, re-parsed with the **current** model, must all be non-`None`.

Directory names do not matter: a cache written with any `case_naming` matches.

!!! warning "What is *not* in the cache key"
    The calculator command, the script content and the output extractors are not part
    of the key. Changing `calc.sh` without changing the inputs still gives cache hits.
    Declare a `code_id` / `version_cmd` in calculator aliases
    ([Caching](../running/caching.md#cache-identity-code_id)), or run into a fresh
    `results_dir` without `cache://`.

- Caches written by fz versions using the previous MD5 format are ignored unless
  `FZ_CACHE_ACCEPT_LEGACY=1`.
- `fzr` pointed at an existing `results_dir` renames it with a timestamp
  (`run1_2026-09-30_20-17-13`) before running. The special entry **`cache://_`** means
  "the previous content of `results_dir`" and is redirected to that renamed copy.
  `cache://run1` with `results_dir="run1"` finds nothing: it points to the new, empty
  directory.

## Common uses

=== "Resume an interrupted run"

    ```python
    fz.fzr("input.txt", {"p": list(range(100))}, model,
           calculators="sh://bash calc.sh", results_dir="run1")
    # Ctrl+C after 50 cases ...
    fz.fzr("input.txt", {"p": list(range(100))}, model,
           calculators=["cache://_", "sh://bash calc.sh"], results_dir="run1")
    # cache://_ = previous content of run1 (renamed run1_<timestamp>)
    ```

=== "Extend a design"

    ```python
    fz.fzr("input.txt", {"t": [100, 200, 300]}, model,
           calculators="sh://bash calc.sh", results_dir="study1")
    fz.fzr("input.txt", {"t": [100, 200, 300, 400, 500]}, model,
           calculators=["cache://study1", "sh://bash calc.sh"], results_dir="study2")
    # 3 reused, 2 computed
    ```

=== "Re-parse without re-running"

    To only change output extractors, `fzo` on the old results is simpler than a
    cached `fzr`: `fz.fzo("study1/*", new_model)`.

## See also

[Caching](../running/caching.md) · [Interrupt & Resume](../running/interrupts.md) ·
[Results & Traceability](../running/results.md)
