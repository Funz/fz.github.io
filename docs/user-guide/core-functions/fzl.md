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
      "supported_calculators": ["sh://"],
      "check_status": "passed"
    }
  },
  "calculators": {
    "sh://": {"supports_models": "all", "check_status": "failed",
              "check_error": "Empty sh:// command"}
  }
}
```

## Limitations

- Calculators are listed by their `uri`, not by alias file name.
- An alias whose command is in its `models` map — `{"uri": "sh://", "models":
  {"perfectgas": "bash calculate.sh"}}`, the layout used by installed wrappers — is
  reported `failed` / `Empty sh:// command` by `--check`, although `fzr` runs it
  correctly. Check such an alias with a real run: `fzr ... --model perfectgas` without
  `--calculators`.
- Algorithms are not listed: use `ls .fz/algorithms ~/.fz/algorithms` or
  `fz.list_installed_algorithms()`.

## See also

[.fz Directory & Aliases](../../reference/configuration.md) ·
[Installing Models & Algorithms](../installing.md) ·
[Calculators](../calculators/overview.md)
