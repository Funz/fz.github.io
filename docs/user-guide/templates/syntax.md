# Input Template Syntax

A template is the simulation code's normal input file (or directory of files) in which
some values are replaced by **variables** and **formulas**. The markers are configured
in the [model](../models/definition.md); this page uses `varprefix="$"`,
`formulaprefix="@"`, `delim="{}"`, `commentline="#"`.

!!! warning "Set `delim` explicitly"
    A model **without** a `delim` key delimits variables with `()` and formulas with `{}`
    (the Java Funz convention). With such a model `${x}` is **not** a variable — only `$x`
    and `$(x)` are. The CLI used without `--model` applies `delim: "{}"`, so the same
    template can behave differently from Python and from the CLI.

## Variables

| Syntax | Meaning |
|--------|---------|
| `$name` | Variable. The name is `[A-Za-z_][A-Za-z0-9_]*`, case-sensitive, and ends at the first other character. |
| `${name}` | Same, delimited: `${T}_celsius` is the variable `T` followed by `_celsius`. |
| `${name~default}` | Variable with a default value, used when `name` is not given (a warning is logged). |

```text title="input.txt"
mesh_size = ${mesh~100}
time_step = $dt
output    = run_${case_id}.dat
```

A variable that is neither provided nor defaulted is **left unchanged** in the compiled
file (no error from `fzc`). `fzr` refuses to run when `input_variables` is omitted but
the template declares variables.

Values are inserted as text (`str(value)`): `1.0` stays `1.0`, `1` stays `1`.

## Formulas

`@{expression}` is replaced by the value of the expression, evaluated when the case is
compiled. Variables used inside a formula keep their prefix:

```text
T_kelvin = @{$T_celsius + 273.15}
area     = @{math.pi * $r ** 2}
ratio    = @{$a / $b | 0.000}          # formatted with a DecimalFormat pattern
```

The interpreter is Python by default, R with `"interpreter": "R"` (or
`FZ_INTERPRETER=R`). Number formats (`| 0.00`, `| #.###`, `| 0.00E00`) are described in
[Formulas](formulas.md).

## Context lines (`#@`)

Lines starting with `commentline` + `formulaprefix` (`#@`) hold code executed before the
formulas: imports, constants, functions. They may reference variables.

```text
#@ import math
#@ R = 8.314
#@ def L_to_m3(L):
#@     return L / 1000
V_m3 = @{L_to_m3($V_L)}
P    = @{$n_mol * R * ($T_celsius + 273.15) / L_to_m3($V_L)}
```

- `#@: code` (colon) declares a **static** object: it is also reported by `fzi` with its
  value (e.g. `#@: K = 10` → `'K': '10'`).
- `#@? ...` lines are Java Funz unit tests and are skipped.
- Context lines stay in the compiled file with variables substituted; the code must
  accept them as comments. Change `commentline` if `#` is not a comment for the code.

## What `fzi` reports

`fzi` returns a dict whose keys are the variables, the static objects and the formula
expressions found:

```text
a=${a~3}
b=$b
#@: K = 10
c=@{$a*2}
```

```python
fz.fzi("input.txt", {"delim": "{}"})
# {'K': '10', 'a': 3, 'b': None, 'a*2': 6}
```

Variables map to `None` or their default; formulas map to their value when it can be
computed from defaults, `None` otherwise. The inputs to provide are the variable names,
not the formula keys.

## Directories of input files

`input_path` may be a directory: every file is scanned and compiled, the tree structure
is kept, and the calculator runs inside the per-case copy of the tree (e.g. an OpenFOAM
case with `system/`, `constant/`, `0/`). Large files identical for every case should be
passed with [`input_static`](../running/results.md#shared-static-files-input_static)
instead.

## Choosing markers

Change the markers when they collide with the code's own syntax: a `$` used by the
code's macros makes `fzi` report unexpected variables.

| Code syntax conflict | Model change |
|----------------------|--------------|
| `$` used by the code | `"varprefix": "%"` |
| `#` is not a comment | `"commentline": "//"` (or `"!"`, `"*"`, `"C "`...) |
| `{}` used by the code | `"delim": "()"` or `"[]"` |

Real wrappers illustrate the range: MCNP uses `%(...)` with `C ` comments, Scale
`&(...)` with `'` comments, Telemac `$(...)` with `/` comments ([Plugins](../../plugins/index.md)).

## Java Funz templates

Java Funz templates use `$(var)` and `@{expr}` — the defaults when the model has no
`delim`. `$(var~default;comment;bounds)` is accepted (only the default is used). A
template marking variables with `?var` needs `"varprefix": "?"`; there is no automatic
`?var` → `$var` conversion.

## See also

- [Formulas](formulas.md) — interpreters, R, number formatting
- [Model Definition](../models/definition.md) — all model fields and defaults
- [fzi](../core-functions/fzi.md), [fzc](../core-functions/fzc.md)
