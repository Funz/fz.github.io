# Parallel Execution

FZ runs cases concurrently across the calculators you provide. Each calculator entry is
locked to one case at a time, so **N calculator entries = N parallel workers**.

## Turning On Parallelism

```python
# Sequential — one calculator entry
fz.fzr("input.txt", {"t": [100, 200, 300, 400, 500]}, model,
       calculators="sh://bash calc.sh")

# Parallel — repeat the entry
fz.fzr("input.txt", {"t": [100, 200, 300, 400, 500]}, model,
       calculators=["sh://bash calc.sh"] * 3)   # 3 cases at once
```

The entries do not have to be identical — mix local, SSH, and SLURM freely:

```python
calculators = [
    "sh://bash calc.sh",
    "sh://bash calc.sh",
    "ssh://user@node1/bash /path/calc.sh",
    "ssh://user@node2/bash /path/calc.sh",
]
```

## Load Balancing

Cases are handed out round-robin. With 10 cases and 3 calculators:

| Calculator | Cases |
|------------|-------|
| 0 | 0, 3, 6, 9 |
| 1 | 1, 4, 7 |
| 2 | 2, 5, 8 |

## Controlling the Worker Count

| Method | Example |
|--------|---------|
| Number of calculator entries | `["sh://bash calc.sh"] * 8` |
| Environment variable | `export FZ_MAX_WORKERS=8` |
| Config object | `from fz import get_config; get_config().max_workers = 8` |

`FZ_MAX_WORKERS` caps the thread pool regardless of how many calculator entries you pass.

### Choosing a Number

- **CPU-bound**: about `os.cpu_count()` workers.
- **I/O-bound / remote**: more than the core count can help.
- **Memory-bound**: `available_RAM / RAM_per_case`.

## Progress and Interrupts

A progress bar with ETA is shown on **stderr** (auto-disabled when stderr is not a
terminal, e.g. in CI or when redirected). Press **Ctrl+C** for a graceful shutdown:
running cases finish, no new cases start, partial results are saved. See
[Interrupt Handling](interrupts.md).

## Combine With Cache

```python
calculators = [
    "cache://previous_run",       # instant on a hit
    *["sh://bash calc.sh"] * 4,   # otherwise 4 parallel workers
]
```

## See Also

- [Caching Strategy](caching.md) · [Interrupt Handling](interrupts.md)
- [Calculators Overview](../calculators/overview.md)
- [`FZ_MAX_WORKERS`](../../reference/environment.md#fz_max_workers)
