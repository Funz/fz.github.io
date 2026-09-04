# API Reference

`import fz` exposes six functions. Each has a dedicated guide with full parameters and
examples — this page is the at-a-glance summary.

## Functions

| Function | Signature (essentials) | Returns |
|----------|------------------------|---------|
| [`fzi`](../user-guide/core-functions/fzi.md) | `fzi(input_path, model, input_static=None)` | `dict` — variable names → `None` |
| [`fzc`](../user-guide/core-functions/fzc.md) | `fzc(input_path, input_variables, model, output_dir, input_static=None)` | `None` (writes compiled files) |
| [`fzo`](../user-guide/core-functions/fzo.md) | `fzo(output_dir, model)` | `DataFrame` — one row per case |
| [`fzr`](../user-guide/core-functions/fzr.md) | `fzr(input_path, input_variables, model, calculators, results_dir="results", *, input_static=None, case_naming="path", timeout=None, callbacks=None)` | `DataFrame` — inputs + outputs + `status`/`calculator`/`error`/`command` |
| [`fzd`](../user-guide/core-functions/fzd.md) | `fzd(input_path, input_variables, model, output_expression, algorithm, calculators=None, algorithm_options=None, analysis_dir="analysis", *, input_static=None)` | `dict` — `XY`, `analysis`, `iterations`, `total_evaluations`, `summary` |
| [`fzl`](../user-guide/core-functions/fzl.md) | `fzl(models="*", calculators="*", check=False)` | `dict` — `{"models": ..., "calculators": ...}` |

## Common Arguments

| Argument | Accepted values |
|----------|-----------------|
| `model` | `dict` definition, or a `str` alias resolved from `.fz/models/` |
| `calculators` | a URI `str`, an alias `str`, or a `list` of them — `sh://`, `ssh://`, `slurm://`, `funz://`, `cache://` |
| `input_variables` | `{"x": [1, 2, 3]}` (list → varied), `{"x": 5}` (fixed); for `fzd`, `{"x": "[min;max]"}` ranges |
| `input_static` | `list` of paths identical across every case — never templated or re-hashed per case *(1.2)* |
| `output_expression` | (`fzd`) a `str` expression, or a `list` of expressions for a vector objective *(1.2)* |

## Config Helper

```python
from fz import get_config
config = get_config()          # reads FZ_* environment variables
config.max_workers = 4         # override for the current process
```

## CLI

Every function has a matching command — `fzi`, `fzc`, `fzo`, `fzr`, `fzd`, `fzl` — plus
`fz install` / `fz uninstall` for plugins. Results go to **stdout**, logs and the
progress bar to **stderr**. See [Configuration](configuration.md#argument-formats-cli)
for the accepted argument formats.

## See Also

- [Configuration](configuration.md) · [Environment Variables](environment.md)
- [Model Definition](../user-guide/model-definition.md) · [Calculators Overview](../user-guide/calculators/overview.md)
- Deep dives in the [main FZ repository docs](https://github.com/Funz/fz/tree/main/doc)
