# fzi - Parse Input Variables

`fzi` scans an input file or directory and reports every **variable** it finds — the
placeholders your templates expect you to fill in. It reads nothing else and runs
nothing; it is the discovery step.

## Function Signature

```python
fz.fzi(input_path, model, input_static=None)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `input_path` | `str` | Input file or directory (scanned recursively) |
| `model` | `dict` or `str` | Model definition or alias — only the syntax fields matter here (`varprefix`, `delim`, `formulaprefix`, `commentline`) |
| `input_static` | `list`, optional | Shared files to ignore while scanning — never templated *(1.2)* |

## Returns

A `dict` mapping each variable name to `None` (a template ready to be filled with
values):

```python
model = {"varprefix": "$", "delim": "{}"}
# input.txt:  Temperature: ${temp}, Pressure: ${pressure}

fz.fzi("input.txt", model)
# {'temp': None, 'pressure': None}
```

## Variables vs Formulas

Names that appear only inside a formula (`@{...}`) or that are *defined* in a formula
context line (`#@ ...`) are **not** variables:

```text
n_mol=$n_mol
T_celsius=$T_celsius
#@ T_kelvin = $T_celsius + 273.15
T_kelvin=@{T_kelvin}
```

```python
model = {"varprefix": "$", "formulaprefix": "@", "delim": "{}", "commentline": "#"}
fz.fzi("input.txt", model)
# {'n_mol': None, 'T_celsius': None}   — T_kelvin is a formula result, not an input
```

## Typical Uses

- Discover the parameters of a legacy input deck.
- Validate that you are supplying every value a template needs before an `fzr` run.
- Auto-generate a parameter list for documentation.

## CLI

```bash
fzi input.txt -m mymodel
fzi input_dir/ -m mymodel --format json
```

## See Also

- [fzc](fzc.md) — substitute values into the template
- [fzr](fzr.md) — the full run that calls `fzi` → `fzc` → execute → `fzo`
- [Model Definition](../model-definition.md) · [Formula Evaluation](../advanced/formulas.md)
