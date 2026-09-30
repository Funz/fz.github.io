# fzo - Parse Output

`fzo` runs the model's output extractors in one or several existing directories and
returns one row per directory.

```python
fz.fzo(output_path, model) -> pandas.DataFrame
```

| Parameter | Description |
|-----------|-------------|
| `output_path` | A directory, or a glob such as `results/*` |
| `model` | Model dict, JSON string/file or alias; only `output` is used |

```python
model = {"output": {"pressure": "python://grep(r'pressure = (\\S+)', 'output.txt')"}}

fz.fzo("results/*", model)
#                              path   pressure  T_celsius  V_L
# 0  results/T_celsius=10,V_L=1  2354109.1         10    1
# ...
```

## Columns

- `path`: the directory parsed.
- One column per `output` entry ([Output Extraction](../models/outputs.md)).
- Variable columns recovered from the directory name `var1=val1,var2=val2,...`; with
  `case_naming="hash"`/`"index"` they come from `cases.csv` at the results root, or from
  each case's `info.txt`.
- `_output_error` when an extractor failed.

!!! warning "Target the case directories"
    `fzo("results", model)` runs the extractors in `results/` itself and returns one row
    of `None`. Use `fzo("results/*", model)` or a single case directory.

## CLI

```bash
fzo 'results/*' --model mymodel --format json
fzo results/case_3 --output-cmd 'P=grep "P =" output.txt | cut -d= -f2' --format csv
```

`--format`: `json`, `csv`, `html`, `markdown` (default), `table`. Quote globs so that
fz, not the shell, expands them.

## Use it to

- re-parse a finished study with a new or corrected output definition, without
  re-running it;
- check an extractor on one manually run case before a study.

## See also

[Output Extraction](../models/outputs.md) · [fzr](fzr.md) · [Results & Traceability](../running/results.md)
