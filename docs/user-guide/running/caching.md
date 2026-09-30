# Caching

fz does not recompute a case whose inputs were already computed, provided a
[`cache://`](../calculators/cache.md) entry points to the earlier results. `fzd` adds
automatic caching across its iterations.

## Cache key

Every case directory holds a `.fz_hash` file:

```text title=".fz_hash"
# fz-hash v2
# code_id: telemac@v8p5
98752ee28d5484bdc2814fb70adb6a0b2fb31f6a9b8ee7ae81fd2fc9cf300b3b  input.txt
```

- SHA-256 of each compiled input file and of each `input_static` file;
- optional `code_id` of the calculator that produced the results.

A cached case matches when the hashes are equal, the code identities are compatible,
and all outputs re-parsed with the current model are non-`None`.

**Not in the key:** the calculator command, the script content, the model's output
extractors, the directory name.

## Cache identity (`code_id`)

The same code is often launched differently on each calculator (`bash run.sh` locally,
`/opt/telemac/v8p5/run.sh` over SSH), so the command is not part of the key. To
distinguish code versions, calculator aliases can declare their identity:

```json title=".fz/calculators/cluster.json"
{"uri": "ssh://u@hpc/bash /opt/telemac/v8p5/run.sh", "code_id": "telemac@v8p5"}
```

```json title=".fz/calculators/local.json"
{"uri": "sh://bash ./run.sh", "version_cmd": "./run.sh --version"}
```

| Situation | Result |
|-----------|--------|
| Same `code_id` on both sides | Match, whatever the commands |
| Different `code_id` | Never matches |
| No `code_id` on one or both sides | Match with a one-time warning; refused with `FZ_CACHE_STRICT=1` |
| Cache written in the old MD5 format | Ignored; considered with `FZ_CACHE_ACCEPT_LEGACY=1` (then as "no `code_id`") |

`version_cmd` is run once per calculator per session; its output becomes the `code_id`.

## Patterns

```python
# Extend a study: only new cases are computed
fz.fzr("input.txt", {"T": [10, 20, 30, 40, 50]}, model,
       calculators=["cache://study1", "sh://bash calc.sh"], results_dir="study2")

# Resume in place: cache://_ is the previous content of results_dir
fz.fzr("input.txt", variables, model,
       calculators=["cache://_", "sh://bash calc.sh"], results_dir="study1")

# Several cache sources, then compute
calculators = ["cache://latest", "cache://archive/*", "sh://bash calc.sh"]
```

To force recomputation after changing the code, declare a new `code_id`, or run into a
new `results_dir` without `cache://`.

## fzd

- Points already evaluated in an earlier iteration are not re-run.
- An existing `analysis_dir` is renamed with a timestamp and its iterations are used as
  cache by the new run.

## See also

[Cache calculator](../calculators/cache.md) · [Interrupt & Resume](interrupts.md) ·
[Results & Traceability](results.md)
