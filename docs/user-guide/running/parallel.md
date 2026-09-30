# Parallelism & Retries

## Number of concurrent cases

Each **non-cache calculator entry** runs one case at a time. The number of cases running
concurrently is:

```text
min(number of non-cache calculator entries, number of cases, FZ_MAX_WORKERS if set)
```

```python
calculators = "sh://bash calc.sh"                      # 1: sequential
calculators = ["sh://bash calc.sh"] * 4                # 4 local cases at a time
calculators = ["cache://old"] + ["sh://bash calc.sh"] * 4   # cache entries do not count
calculators = [                                        # 3 at a time, on 3 machines
    "sh://bash calc.sh",
    "ssh://u@node1/bash /opt/run.sh",
    "ssh://u@node2/bash /opt/run.sh",
]
```

An alias counts as one entry: `calculators=["localhost_Moret"] * 4` runs 4 cases at a
time, while omitting `calculators` (auto-discovery of one alias) runs them one by one.

`FZ_MAX_WORKERS` only **lowers** that number; setting it never adds workers. Exception:
`slurm-array://` uses one waiting thread per case (capped by `FZ_MAX_WORKERS`) so that
all cases can be batched into one job array.

For `fzd` with a Python function model, `calculators=N` is the number of threads.

## Assignment of cases

Case *i* first tries entry *i mod n*; if that entry is busy, the first free entry takes
it. With equal durations this is a round-robin distribution; with unequal durations,
faster entries take more cases.

## Retries

When a run fails (non-zero exit, timeout, transfer error), the case is tried again on
the calculators, preferring another entry. After `FZ_MAX_RETRIES` failures (default 5)
the case is marked `failed` with the last error. A case whose command succeeds but whose
outputs cannot be parsed is **not** retried: it keeps its status and the reason goes to
`error` (`Missing output: ...`).

```python
calculators = [
    "sh://bash fast_but_fragile.sh",
    "sh://bash robust.sh",           # tried when the first one fails
]
```

## Setting the limits

```bash
export FZ_MAX_WORKERS=8      # before starting Python
export FZ_MAX_RETRIES=3
```

```python
import os, fz
os.environ["FZ_MAX_WORKERS"] = "8"
fz.reload_config()           # FZ_* variables are read at import time
# or: fz.get_config().max_workers = 8
```

## Choosing the number of entries

- CPU-bound local code: about the number of cores divided by the cores used per case.
- Memory-bound: available memory / memory per case.
- Remote calculators: limited by the remote resources and your quota, not by the local
  machine (fz threads mostly wait).

## Progress

A progress line with ETA is written to stderr (disabled when stderr is not a
terminal). For programmatic progress, use `fzr(..., callbacks={...})`
([fzr callbacks](../core-functions/fzr.md#callbacks)).

## See also

[Timeouts](timeouts.md) · [Caching](caching.md) · [Calculators](../calculators/overview.md)
