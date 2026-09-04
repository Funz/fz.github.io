# Model Definition

A model defines how FZ parses inputs and extracts outputs. See the [main FZ documentation](https://github.com/Funz/fz#model-definition) for complete details.

## Common Fields

| Field | Default | Purpose |
|-------|---------|---------|
| `varprefix` | `$` | Marks a variable in input templates (`$x`, `${x}`, `${x~default}`) |
| `formulaprefix` | `@` | Marks a formula (`@{expr}`) |
| `delim` | `{}` | Delimiters around variable names / formula expressions |
| `commentline` | `#` | Comment marker introducing a formula-context line (`#@ ...`) |
| `interpreter` | `python` | Formula interpreter — `python` or `R` |
| `output` | — | Map of result column → extraction spec (see below) |
| `timeout` | — | Per-model run timeout in seconds; overrides `FZ_RUN_TIMEOUT`. `None`/`0` disables it. (New in 1.2) |

## Output Extraction (updated in 1.2)

Each `output` entry says how to pull one result from a case's files. The spec can be:

- a **shell command** (implicit default, or explicit `bash://`) — `"grep 'P:' out.txt | awk '{print $2}'"`
- `python://<expression>` — native Python, no shell required
- `jq://<filter> <file>` — JSON via [jq](https://jqlang.org/)
- `yq://<filter> <file>` — YAML/JSON/XML/TOML via [mikefarah/yq](https://github.com/mikefarah/yq)
- `xpath://<expr> <file>` — XML via `xmllint --xpath`
- a **Python callable** (Python API only) receiving the case directory as a `pathlib.Path`

Any of these may resolve to a **list** for vector-valued outputs (time series, profiles,
spectra). Full details and helper reference: [fzo — Output Command Forms](core-functions/fzo.md#output-command-forms).
