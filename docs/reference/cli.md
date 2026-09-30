# CLI Reference

Every core function has a command, available standalone or as a subcommand of `fz`:

| Standalone | Subcommand | Function |
|------------|------------|----------|
| `fzi` | `fz input` | [fzi](../user-guide/core-functions/fzi.md) |
| `fzc` | `fz compile` | [fzc](../user-guide/core-functions/fzc.md) |
| `fzo` | `fz output` | [fzo](../user-guide/core-functions/fzo.md) |
| `fzr` | `fz run` | [fzr](../user-guide/core-functions/fzr.md) |
| `fzd` | `fz design` | [fzd](../user-guide/core-functions/fzd.md) |
| `fzl` | `fz list` | [fzl](../user-guide/core-functions/fzl.md) |
| — | `fz install model\|algorithm <source> [--global]` | [Installing](../user-guide/installing.md) |
| — | `fz uninstall model\|algorithm <name> [--global]` | [Installing](../user-guide/installing.md) |
| `fz-mcp` | — | [MCP server](../user-guide/ai-agents.md#mcp-server-fz-mcp) |

All commands accept `--help` and `--version`.

## Options

```text
fzi [input_path] [-i PATH] [-m MODEL] [MODEL FIELDS] [--input_static F] [-f FORMAT]
fzc [input_path] [-i PATH] [-m MODEL] [MODEL FIELDS] [-v VARS] [--input_static F] [-o DIR]
fzo [output_path] [-o PATH] [-m MODEL] [MODEL FIELDS] [-f FORMAT]
fzr [input_path] [-i PATH] [-m MODEL] [MODEL FIELDS] [-v VARS] [-r DIR]
    [--case_naming {path,hash,index}] [-c CALC]... [--input_static F]... [-f FORMAT]
fzd -i PATH -v VARS -m MODEL -e EXPR -a ALGO [-r DIR] [-c CALC] [-o OPTIONS] [--input_static F]
fzl [-m PATTERN] [-c PATTERN] [--check] [-f {json,markdown,table}]
```

| Option | Aliases | Commands | Value |
|--------|---------|----------|-------|
| `input_path` (positional) | `--input_path`, `-i` | fzi, fzc, fzr | File or directory |
| `output_path` (positional) | `--output_path`, `-o` | fzo | Directory or quoted glob |
| `--model` | `-m` | all but fzl | Alias, `.json` file, or inline JSON |
| `--input_variables` | `--variables`, `-v` | fzc, fzr | JSON dict (inline or file) or `a=1,b=[1,2]` |
| `--output_dir` | `--output`, `-o` | fzc | Default `output` |
| `--results_dir` | `--results`, `-r` | fzr | Default `results` |
| `--calculators` | `--calculator`, `-c` | fzr, fzd | URI, alias, JSON file or JSON list; repeatable (fzr) |
| `--case_naming` | | fzr | `path` (default), `hash`, `index` |
| `--input_static` | | fzi, fzc, fzr, fzd | Path or JSON list; repeatable |
| `--format` | `-f` | fzi, fzo, fzr | `json`, `csv`, `html`, `markdown` (default), `table` |
| `--format` | `-f` | fzl | `json`, `markdown` (default), `table` |
| `--input_dir` | `--input_path`, `-i` | fzd | Required |
| `--input_vars` | `--input_variables`, `--variables`, `-v` | fzd | JSON with `"[min;max]"` strings, or `x=[0;1],y=2` |
| `--output_expression` | `-e` | fzd | One expression |
| `--algorithm` | `-a` | fzd | Name or path |
| `--options` | `-o` | fzd | JSON (inline or file) |
| `--results_dir` | `-r` | fzd | Default `results_fzd` |

**Model fields** (fzi, fzc, fzo, fzr) define or override the model inline:
`--varprefix`, `--formulaprefix`, `--delim`, `--commentline`, `--interpreter`, and
repeatable `--output-cmd NAME=COMMAND`. Without `--model`, these start from
`{"varprefix": "$", "formulaprefix": "@", "delim": "{}", "commentline": "#"}`.

## Conventions

- Results go to **stdout**; logs (`FZ_LOG_LEVEL`), progress and errors to **stderr**.
  Use `--format json` for machine-readable output.
- Exit status is non-zero on error; `fzr` exits 1 when no case ends `done`.
- `--model`, `--input_variables`, `--options` accept inline JSON or a JSON file;
  `--model` and `--calculators` also accept an alias name from `.fz/`.

## Differences with the Python API

| Feature | Python | CLI |
|---------|--------|-----|
| Explicit list of cases (DataFrame) | yes | no (dict only, full factorial) |
| Multi-objective `fzd` (list of expressions) | yes | no |
| Function model for `fzd` | yes | no |
| Callbacks | yes | no |
| `timeout` per call | `timeout=` | no option: model `timeout` or `FZ_RUN_TIMEOUT` |
| `fzd` default directory | `analysis` | `results_fzd` |
| `fzd` output format | dict | printed summary, no `--format` |
| Model without `delim` | variables use `()` | `{}` when `--model` is absent; `()` when `--model` gives a model without `delim` |

## Shell completion

Completion scripts for bash and zsh are in the fz repository under
[`completions/`](https://github.com/Funz/fz/tree/main/completions).
