# fzr - Run a Parametric Study

`fzr` compiles every case, runs it on the calculators, parses the outputs and returns a
DataFrame. It is `fzc` + execution + `fzo` for a whole design.

```python
fz.fzr(
    input_path,
    input_variables=None,
    model=None,
    results_dir="results",
    calculators=None,
    callbacks=None,
    timeout=None,
    case_naming=None,
    input_static=None,
) -> pandas.DataFrame
```

!!! danger "Pass `calculators` and `results_dir` by keyword"
    `results_dir` is the **4th** positional parameter. `fz.fzr("in.txt", vars, model,
    "sh://bash run.sh")` raises `ValueError` because the value looks like a calculator
    URI (fz ≤ 1.2 used it as a directory name and ran without calculator).

## Parameters

| Parameter | Description |
|-----------|-------------|
| `input_path` | Template file or directory |
| `input_variables` | Design: dict (factorial) or DataFrame (one row per case). Optional when the template has no variables — then pass `model=` by keyword |
| `model` | Model dict, JSON string/file or alias ([Model Definition](../models/definition.md)) |
| `results_dir` | Results root (default `results`); an existing one is renamed with a timestamp |
| `calculators` | URI, alias, dict, or list of them. Omitted: installed aliases matching the model `id`, else `sh://` ([Calculators](../calculators/overview.md)) |
| `callbacks` | Dict of progress callbacks (below) |
| `timeout` | Seconds per case (`0` = no timeout); overrides the model's `timeout` and `FZ_RUN_TIMEOUT` ([Timeouts](../running/timeouts.md)) |
| `case_naming` | `"path"` (default, or `FZ_CASE_NAMING`), `"hash"`, `"index"` ([Results](../running/results.md#case-directory-naming)) |
| `input_static` | Files identical for every case, never templated ([Results](../running/results.md#shared-static-files-input_static)) |

## Designs

```python
# Full factorial: lists are crossed, scalars are fixed (3 x 2 = 6 cases)
fz.fzr("input.txt", {"T": [10, 20, 30], "P": [1, 10], "V": 1.0}, model,
       calculators="sh://bash calc.sh")

# Explicit cases: one row per case (LHS, imported plan, constrained combinations)
import pandas as pd
design = pd.DataFrame({"T": [10, 20, 10], "P": [1, 1, 10]})
fz.fzr("input.txt", design, model, calculators="sh://bash calc.sh")

# numpy arrays are accepted as lists
import numpy as np
fz.fzr("input.txt", {"T": np.linspace(0, 100, 11)}, model, calculators="sh://bash calc.sh")
```

## Result

One row per case, in design order:

| Column | Content |
|--------|---------|
| variables | The case's values |
| outputs | One column per `output` entry (dict outputs expand to `name_key` columns) |
| `path` | Case result directory |
| `status` | `done`, `failed`, `error`, `timeout` or `interrupted`; `done` only means the run ended: check the outputs or `error` |
| `calculator` | Calculator used (`cache://...` for a cache hit), with a short id suffix |
| `error` | Error message, including `Missing output: ...` when an extractor failed |
| `command` | Command actually executed (paths made absolute) |

```python
failed = results[results["status"] != "done"]
print(failed[["path", "status", "error"]])
```

Each case directory contains the compiled inputs, the files written by the code, and
`out.txt`, `err.txt`, `log.txt`, `info.txt`, `history.txt`, `.fz_hash`. The results root
contains `manifest.json` and `ro-crate-metadata.json`. See
[Results & Traceability](../running/results.md).

## Calculators

```python
calculators="sh://bash calc.sh"                        # 1 case at a time
calculators=["sh://bash calc.sh"] * 4                  # 4 at a time
calculators=["cache://previous", "sh://bash calc.sh"]  # reuse, then compute
calculators="cluster"                                  # alias in .fz/calculators/
```

Failed attempts are retried on the calculators, up to `FZ_MAX_RETRIES` (default 5)
failures per case. See [Parallelism & Retries](../running/parallel.md).

## Callbacks

`callbacks` is a **dict** with any of these keys (others raise `ValueError`):

| Key | Arguments |
|-----|-----------|
| `on_start` | `(total_cases, calculators)` |
| `on_case_start` | `(case_index, total_cases, var_combo)` |
| `on_case_complete` | `(case_index, total_cases, var_combo, status, result)` |
| `on_progress` | `(completed, total, eta_seconds)` |
| `on_complete` | `(total_cases, completed_cases, results_df)` |

```python
def done(i, n, combo, status, result):
    print(f"[{i + 1}/{n}] {combo} -> {status}")

fz.fzr("input.txt", {"x": [1, 2, 3]}, model,
       calculators="sh://bash calc.sh",
       callbacks={"on_case_complete": done})
```

Callbacks run in worker threads; an exception raised in a callback is logged and the run
continues.

## Interrupting

The first Ctrl+C stops starting new cases, terminates the running ones, and makes `fzr`
**return** the DataFrame (interrupted cases have `status="interrupted"`); a second Ctrl+C
raises `KeyboardInterrupt`. Resume with `cache://`. See
[Interrupt & Resume](../running/interrupts.md).

## CLI

```bash
fzr input.txt --model mymodel \
    --input_variables '{"T": [10, 20, 30], "P": [1, 10]}' \
    --calculators '["cache://results_v1", "sh://bash calc.sh"]' \
    --results_dir results_v2 --case_naming hash --format json
```

- `--calculators` / `-c` is repeatable and also accepts an alias, a JSON file or an
  inline JSON list.
- `--input_variables` accepts a JSON dict (inline or file) or the short form
  `'T=[10,20,30],P=1'`. A list of cases (non-factorial design) is Python-only: pass a
  DataFrame.
- No option sets a timeout: use the model's `timeout` or `FZ_RUN_TIMEOUT`.
- Exit status 1 when no case ends with `status="done"`.

## See also

[fzc](fzc.md) · [fzo](fzo.md) · [fzd](fzd.md) · [Calculators](../calculators/overview.md) ·
[Constraints & Limits](../../reference/limitations.md)
