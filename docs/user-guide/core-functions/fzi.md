# fzi - Parse Input

`fzi` scans a template (file or directory) and reports the variables, static objects
and formulas it contains. It runs nothing.

```python
fz.fzi(input_path, model, input_static=None) -> dict
```

| Parameter | Description |
|-----------|-------------|
| `input_path` | Template file or directory (scanned recursively) |
| `model` | Model dict, JSON string/file or alias; only the syntax fields are used |
| `input_static` | Files excluded from scanning ([shared static files](../running/results.md#shared-static-files-input_static)) |

## Result

A dict whose keys are:

- each **variable** → `None`, or its `~default`;
- each **static object** declared with `#@:` → its value;
- each **formula expression** → its value when computable from defaults, else `None`.

```text title="input.txt"
a=${a~3}
b=$b
#@: K = 10
c=@{$a*2}
```

```python
fz.fzi("input.txt", {"delim": "{}"})
# {'K': '10', 'a': 3, 'b': None, 'a*2': 6}
```

The variables to provide to `fzc`/`fzr` are the variable names (`a`, `b`), not the
formula keys.

## CLI

```bash
fzi input.txt --model mymodel --format json
fzi case_dir/ --delim '{}' --format json        # inline model fields, no alias
```

`--format`: `json`, `csv`, `html`, `markdown` (default), `table`.

## Use it to

- check that the model's markers match the template: stray variables mean `varprefix`
  collides with the code's syntax; missing `${x}` or `$(x)` variables mean `delim` is set
  to the other pair
  ([defaults](../models/definition.md#default-delimiters));
- list the parameters of an existing input deck.

## See also

[Input Template Syntax](../templates/syntax.md) · [fzc](fzc.md) · [fzr](fzr.md)
