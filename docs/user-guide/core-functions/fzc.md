# fzc - Compile

`fzc` substitutes values into a template and evaluates its formulas, writing one
compiled copy per case. It runs nothing: use it to check compilation before a study.

```python
fz.fzc(input_path, input_variables=None, model=None, output_dir="output",
       input_static=None) -> None
```

| Parameter | Description |
|-----------|-------------|
| `input_path` | Template file or directory |
| `input_variables` | `{"x": 1}` (fixed) or `{"x": [1, 2]}` (one case per value, Cartesian product); may be omitted when the template has no variables |
| `model` | Model dict, JSON string/file or alias |
| `output_dir` | Destination (default `output`) |
| `input_static` | Shared files, linked rather than templated |

## Output layout

When the template declares variables, **each case gets a sub-directory named after its
values, even when all values are scalars**:

```python
fz.fzc("input.txt", {"T": 25, "P": 1.0}, {"delim": "{}"}, "compiled")
# compiled/T=25,P=1.0/input.txt

fz.fzc("input.txt", {"T": [10, 20], "P": [1, 10], "V": 1.0}, {"delim": "{}"}, "grid")
# grid/T=10,P=1,V=1.0/input.txt
# grid/T=10,P=10,V=1.0/input.txt
# grid/T=20,P=1,V=1.0/input.txt
# grid/T=20,P=10,V=1.0/input.txt
```

- An existing `output_dir` is renamed with a timestamp suffix before writing.
- Each case directory also receives `.fz_hash` (SHA-256 of the compiled files).
- A variable that is neither given nor defaulted is left unchanged in the file.
- A template without variables is compiled directly into `output_dir/`.

To test a compiled case by hand, run the code **inside the case sub-directory** and
point `fzo` at it (or at `compiled/*`), not at `compiled/`.

## Formulas

```text
Temperature: $T_celsius C
#@ T_kelvin = $T_celsius + 273.15
Calculated T: @{T_kelvin | 0.00} K
```

gives, for `T_celsius=25`:

```text
Temperature: 25 C
#@ T_kelvin = 25 + 273.15
Calculated T: 298.15 K
```

Context lines stay in the file (with variables substituted). See
[Formulas](../templates/formulas.md).

## CLI

```bash
fzc input.txt --model mymodel \
    --input_variables '{"T": [10, 20], "P": 1.0}' --output_dir compiled/
```

`--input_variables` accepts inline JSON or a JSON file and may be omitted for a
template without variables; `fzc` has no `--format` option.

## See also

[fzi](fzi.md) · [fzo](fzo.md) · [fzr](fzr.md) · [Input Template Syntax](../templates/syntax.md)
