# Model Definition

A **model** describes a simulation code for fz: how variables and formulas are marked in
its input files, and how to extract results from its output files. It is a Python `dict`,
a JSON string, a JSON file, or an alias stored in `.fz/models/<name>.json`.

!!! note "A model never says how to run the code"
    There is no `run` or `command` field. Where and how the code runs is given by the
    [calculator](../calculators/overview.md). Forgetting the calculator makes fz fall back
    to `sh://` with no command, which tries to execute the input file itself; the symptom
    is `Permission denied ... ./input.txt`.

## Example

```json title=".fz/models/perfectgas.json"
{
  "id": "perfectgas",
  "varprefix": "$",
  "formulaprefix": "@",
  "delim": "{}",
  "commentline": "#",
  "interpreter": "python",
  "timeout": 1800,
  "output": {
    "pressure": "python://grep(r'pressure = (\\S+)', 'output.txt')"
  }
}
```

```python
fz.fzr("input.txt", variables, "perfectgas", calculators="sh://bash calc.sh")
```

## Fields

| Field | Default | Role |
|-------|---------|------|
| `varprefix` | `$` | Variable marker: `$x` |
| `formulaprefix` | `@` | Formula marker: `@{expr}` |
| `delim` | see below | Two characters (or `""`) delimiting variables *and* formulas |
| `var_delim` / `formula_delim` | `()` / `{}` | Delimiters of variables / formulas separately; take precedence over `delim` |
| `commentline` | `#` | Comment marker; `commentline` + `formulaprefix` (`#@`) starts a context line |
| `interpreter` | `FZ_INTERPRETER` (`python`) | `python` or `R` for formulas |
| `output` | — | Map *column name* → extractor; required to get results ([Output Extraction](outputs.md)) |
| `timeout` | — | Per-case run timeout in seconds; `null` or `0` disables it ([Timeouts](../running/timeouts.md)) |
| `id` | — | Identifier matched against calculator aliases' `models` keys, for auto-discovery |

Accepted aliases of the key names (first found wins): `var_prefix`, `varprefix`,
`var_char`, `varchar`; `formula_prefix`, `formulaprefix`, `form_prefix`, `formprefix`,
`formula_char`, `form_char`; `commentline`, `comment_line`, `comment_char`,
`commentchar`, `comment`.

### Default delimiters

| Model contains | Variables | Formulas |
|----------------|-----------|----------|
| `"delim": "{}"` | `$x`, `${x}` | `@{...}` |
| `"delim": "()"` | `$x`, `$(x)` | `@(...)` |
| no `delim`, no `var_delim`/`formula_delim` | `$x`, `$(x)` — **not** `${x}` | `@{...}` |
| CLI without `--model` | `$x`, `${x}` | `@{...}` |

`delim` must be empty or exactly two characters (validated). Setting it explicitly
avoids the difference between the Python default and the CLI default.

## Where a model can come from

| Form | Example |
|------|---------|
| `dict` (Python) | `model={"delim": "{}", "output": {...}}` |
| JSON string | `--model '{"delim": "{}", "output": {...}}'` |
| JSON file (path ending in `.json`) | `--model models/perfectgas.json` |
| Alias | `--model perfectgas` → `./.fz/models/perfectgas.json`, then `~/.fz/models/perfectgas.json` |

An alias file's name does **not** set its `id`: add `"id"` in the JSON for calculator
auto-discovery to work (installed wrappers do).

## Inline model on the CLI

Model fields can be given as flags instead of, or on top of, `--model`:

```bash
fzo results/ --delim '{}' --output-cmd 'pressure=grep "P =" output.txt | cut -d= -f2'
```

`--varprefix`, `--formulaprefix`, `--delim`, `--commentline`, `--interpreter` and
repeatable `--output-cmd NAME=COMMAND` are available on `fzi`, `fzc`, `fzo`, `fzr`.

## Checking a model

```bash
fzi input.txt --model perfectgas --format json   # exactly the expected variables?
fz list --models perfectgas --check              # alias found and valid?
```

Unexpected variables in `fzi` usually mean `varprefix` collides with the code's own
syntax.

## See also

- [Input Template Syntax](../templates/syntax.md) · [Formulas](../templates/formulas.md)
- [Output Extraction](outputs.md)
- [Installing Models](../installing.md) — ready-made models for known codes
- [.fz Directory & Aliases](../../reference/configuration.md)
