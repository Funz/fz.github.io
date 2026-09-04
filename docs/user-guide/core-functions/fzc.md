# fzc - Compile Input Files

`fzc` turns a template into ready-to-run input files: it substitutes variable values and
evaluates formulas. With list-valued variables it writes one compiled case per
combination (the Cartesian product).

## Function Signature

```python
fz.fzc(input_path, input_variables, model, output_dir, input_static=None)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `input_path` | `str` | Template file or directory |
| `input_variables` | `dict` | Values — scalar (fixed) or list (varied) |
| `model` | `dict` or `str` | Model definition or alias |
| `output_dir` | `str` | Where compiled files are written |
| `input_static` | `list`, optional | Shared files symlinked into `output_dir` rather than templated/duplicated *(1.2)* |

Returns `None`; the result is the files written under `output_dir`.

## Single Case

```python
model = {"varprefix": "$", "formulaprefix": "@", "delim": "{}", "commentline": "#"}

fz.fzc("input.txt", {"temp": 25, "pressure": 101.3}, model, "compiled/")
# compiled/input.txt  — values substituted
```

## Grid of Cases

```python
fz.fzc(
    "input.txt",
    {"temp": [10, 20, 30], "pressure": [1, 10], "volume": 1.0},  # 3 × 2 × fixed
    model,
    "compiled_grid/",
)
# compiled_grid/temp=10,pressure=1/input.txt
# compiled_grid/temp=10,pressure=10/input.txt
# ... 6 directories total
```

## Formulas

```text
Temperature: $T_celsius C
#@ T_kelvin = $T_celsius + 273.15
Temperature: @{T_kelvin | 0.00} K
```

Formula context lines (`#@ ...`) are evaluated first, then `@{...}` expressions are
replaced. See [Formula Evaluation](../advanced/formulas.md), including the 1.2
`DecimalFormat` number-formatting patterns.

## CLI

```bash
fzc input.txt -m mymodel -v '{"temp": [10, 20, 30], "pressure": 1.0}' -o compiled/
```

Since **1.2**, `--input_variables` may be omitted when the template declares no
variables.

## See Also

- [fzi](fzi.md) — find the variables first
- [fzo](fzo.md) — parse the outputs afterwards
- [fzr](fzr.md) — do all of it in one call
- [Model Definition](../model-definition.md)
