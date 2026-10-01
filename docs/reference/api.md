# Python API

```python
import fz
```

## Core functions

| Function | Signature | Returns |
|----------|-----------|---------|
| [`fzi`](../user-guide/core-functions/fzi.md) | `fzi(input_path, model, input_static=None)` | `dict` of variables / static objects / formulas |
| [`fzc`](../user-guide/core-functions/fzc.md) | `fzc(input_path, input_variables=None, model=None, output_dir="output", input_static=None)` | `None` (writes files) |
| [`fzo`](../user-guide/core-functions/fzo.md) | `fzo(output_path, model)` | `DataFrame`, one row per directory |
| [`fzr`](../user-guide/core-functions/fzr.md) | `fzr(input_path, input_variables=None, model=None, results_dir="results", calculators=None, callbacks=None, timeout=None, case_naming=None, input_static=None)` | `DataFrame`, one row per case |
| [`fzd`](../user-guide/core-functions/fzd.md) | `fzd(input_path, input_variables, model, output_expression, algorithm, calculators=None, algorithm_options=None, analysis_dir="analysis", input_static=None)` | `dict` with `XY`, `analysis`, `algorithm`, `iterations`, `total_evaluations`, `summary` |
| [`fzl`](../user-guide/core-functions/fzl.md) | `fzl(models="*", calculators="*", check=False)` | `dict` with `models`, `calculators` |

!!! danger "Keyword arguments"
    In `fzr`, `results_dir` precedes `calculators`. Always write `calculators=...` and
    `results_dir=...`.

Invalid argument types raise `TypeError`; invalid values (unknown `case_naming`, bad
`delim`, unknown callback name, duplicate DataFrame rows, missing `input_variables` for a
template with variables, negative `timeout`, a `results_dir` that looks like a
calculator URI) raise `ValueError`; a missing `input_path` raises
`FileNotFoundError`.

## Installation of models and algorithms

| Function | Role |
|----------|------|
| `install_model(source, global_install=False)` | Install from name, URL or zip; returns names and paths |
| `install(model, global_install=False)` | Same as `install_model` |
| `uninstall_model(model_name, global_uninstall=False)` | Remove |
| `list_installed_models(global_list=False)` | Installed models |
| `install_algorithm(source, global_install=False)` | Install an algorithm |
| `uninstall_algorithm(algorithm_name, global_uninstall=False)` | Remove |
| `list_installed_algorithms(global_list=False)` | Installed algorithms |
| `list_models(global_list=False)` | Model aliases |

## Configuration and logging

| Function | Role |
|----------|------|
| `get_config()` | Current configuration object (`max_workers`, `max_retries`, `run_timeout`, `case_naming`, ...), modifiable at runtime |
| `reload_config()` | Re-read the `FZ_*` environment variables (they are otherwise read once, at import) |
| `print_config()` | Print the effective configuration |
| `set_log_level(level)` / `get_log_level()` | `"QUIET"`, `"ERROR"`, `"WARNING"`, `"INFO"`, `"DEBUG"` |
| `set_interpreter(name)` / `get_interpreter()` | Default formula interpreter (`"python"` or `"R"`) |

## Other

| Name | Role |
|------|------|
| `discover_funz_servers(udp_port, listen_duration=10.0, stop_when=None)` | List Java Funz calculators broadcasting on a UDP port |
| `FunctionModelParallelError` | Raised by `fzd` when a function model fails while evaluated in parallel |

Everything else (`fz.helpers`, `fz.runners`, `fz.io`, ...) is internal and may change.

## See also

[CLI Reference](cli.md) · [Environment Variables](environment.md)
