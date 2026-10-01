# fzl - List Models and Calculators

`fzl` (or `fz list`) lists the model and calculator aliases found in `./.fz/` and
`~/.fz/`, which calculators support which model, and optionally checks them.

```python
fz.fzl(models="*", calculators="*", check=False) -> dict
```

```bash
fzl [--models PATTERN] [--calculators PATTERN] [--check] [--format json|markdown|table]
fz list ...        # same
```

| Option | Meaning |
|--------|---------|
| `--models`, `-m` | Glob on model alias names (default `*`) |
| `--calculators`, `-c` | Glob or regex on calculator alias names (default `*`) |
| `--check` | Validate each model (JSON structure) and calculator (test run) |
| `--format`, `-f` | `markdown` (default), `json`, `table` — no `csv`/`html` |

## Result

```json
{
  "models": {
    "perfectgas": {
      "path": "/project/.fz/models/perfectgas.json",
      "properties": {"id": "perfectgas", "delim": "{}", "output": {"pressure": "..."}},
      "supported_calculators": ["localhost_perfectgas"],
      "check_status": "passed"
    }
  },
  "calculators": {
    "localhost_perfectgas": {
      "path": "/project/.fz/calculators/localhost_perfectgas.json",
      "uri": "sh://",
      "supports_models": ["perfectgas"],
      "check_status": "passed"
    }
  }
}
```

- Calculator aliases are keyed by file name; a project alias shadows a global one with
  the same name. With no alias installed, the default `sh://` is listed.
- `--check` validates each command of an alias's `models` map (`uri` + command).
- Algorithms are not listed: use `ls .fz/algorithms ~/.fz/algorithms` or
  `fz.list_installed_algorithms()`.

!!! note "fz ≤ 1.2"
    Calculators were listed by `uri` (`sh://`) and aliases of the form
    `{"uri": "sh://", "models": {...}}` — the layout of installed wrappers — were
    reported `failed` / `Empty sh:// command` by `--check`.

## See also

[.fz Directory & Aliases](../../reference/configuration.md) ·
[Installing Models & Algorithms](../installing.md) ·
[Calculators](../calculators/overview.md)
