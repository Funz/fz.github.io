# Configuration

FZ is configured through **environment variables**, **`.fz/` alias directories**, and
per-call arguments. Nothing needs to be configured to get started — every setting has a
default.

## Environment Variables

The full list, with defaults, is on the [Environment Variables](environment.md) page.
The most common ones:

| Variable | Purpose | Default |
|----------|---------|---------|
| `FZ_LOG_LEVEL` | `DEBUG` / `INFO` / `WARNING` / `ERROR` / `CRITICAL` | `ERROR` |
| `FZ_MAX_WORKERS` | Thread-pool size for parallel cases | CPU count |
| `FZ_MAX_RETRIES` | Calculator retry attempts per case | `5` |
| `FZ_RUN_TIMEOUT` | Per-case timeout, seconds (`0` disables) | `3600` |
| `FZ_INTERPRETER` | Default formula interpreter (`python` / `R`) | `python` |
| `FZ_SHELL_PATH` | Extra search path for shell binaries | system `PATH` |
| `FZ_CASE_NAMING` | Case dir naming (`path` / `hash` / `index`) | `path` |
| `FZ_CACHE_DIR` | Cache location | `.fz/cache` |

```python
from fz import get_config

config = get_config()
print(config.max_workers, config.max_retries)
config.max_workers = 4          # override at runtime
```

## `.fz/` Directory

FZ looks for aliases in `./.fz/` (project) then `~/.fz/` (user); project wins.

```
.fz/
├── models/          # model aliases      →  fz.fzr(..., model="perfectgas")
│   └── perfectgas.json
├── calculators/     # calculator aliases →  fz.fzr(..., calculators="cluster")
│   └── cluster.json
├── algorithms/      # fzd algorithm plugins
│   ├── brent.py
│   └── pso.R
└── tmp/             # per-run scratch dirs (auto-created)
```

### Model Alias

```json title=".fz/models/perfectgas.json"
{
  "varprefix": "$",
  "formulaprefix": "@",
  "delim": "{}",
  "commentline": "#",
  "interpreter": "python",
  "output": {
    "pressure": "python://grep(r'P = (\\S+)', 'output.txt')"
  }
}
```

### Calculator Alias

```json title=".fz/calculators/cluster.json"
{
  "uri": "ssh://user@hpc.university.edu",
  "models": {
    "perfectgas": "bash /home/user/codes/perfectgas/run.sh",
    "cfd":        "bash /home/user/codes/cfd/run.sh"
  }
}
```

```python
fz.fzr("input.txt", variables, "perfectgas", calculators="cluster")
# resolves to: ssh://user@hpc.university.edu/bash /home/user/codes/perfectgas/run.sh
```

Inspect and validate what is installed with [`fzl`](../user-guide/core-functions/fzl.md):

```bash
fzl --models "*" --calculators "*" --check --format markdown
```

## Timeout Resolution Order

Highest priority first:

1. `timeout=` argument to `fzr()` / `fzc()` (or `--timeout` on the CLI)
2. Model field `model["timeout"]` (int seconds; `None`/`0` disables)
3. `FZ_RUN_TIMEOUT` (default `3600`)

## Argument Formats (CLI)

`--model`, `--calculator`, and `--variables` each accept, tried in this order:

1. **Alias** — `--model perfectgas` (from `.fz/models/`)
2. **JSON file** — `--model model.json`
3. **Inline JSON** — `--model '{"varprefix": "$"}'`

## See Also

- [Environment Variables](environment.md) — every variable in detail
- [Model Definition](../user-guide/model-definition.md)
- [Calculators Overview](../user-guide/calculators/overview.md)
