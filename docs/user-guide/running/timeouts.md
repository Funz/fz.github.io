# Timeouts

A timeout bounds the duration of **one run of one case** (for SLURM, including the time
spent in the queue). A case that exceeds it is stopped and gets `status="timeout"`.

## Resolution order

1. `timeout=` argument of `fzr()` (seconds);
2. the model's `"timeout"` entry;
3. `FZ_RUN_TIMEOUT`.

| Calculator | Default when none of the above is set |
|------------|----------------------------------------|
| `sh://`, `funz://` | 3600 s |
| `ssh://`, `slurm://`, `slurm-array://` | **no timeout** (a warning is logged) |

Setting `FZ_RUN_TIMEOUT` explicitly applies it to every calculator type.

## Disabling

| Setting | Effect |
|---------|--------|
| model `"timeout": null` or `"timeout": 0` | no timeout for this model |
| `FZ_RUN_TIMEOUT=0` | **every case times out immediately** |
| `timeout=0` argument | **every case times out immediately** |

To run without limit, use the model entry, or set a large value.

## Examples

```json title=".fz/models/longcode.json"
{"delim": "{}", "timeout": 86400, "output": {"...": "..."}}
```

```python
fz.fzr("input.txt", variables, model, calculators="sh://bash calc.sh", timeout=600)
```

```bash
export FZ_RUN_TIMEOUT=7200      # before starting Python (or fz.reload_config())
```

There is no CLI option for the timeout: use the model entry or `FZ_RUN_TIMEOUT`.

## See also

[Parallelism & Retries](parallel.md) · [Environment Variables](../../reference/environment.md)
