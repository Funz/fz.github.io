# .fz Directory & Aliases

fz looks for named models, calculators and algorithms in two `.fz/` directories:

1. `./.fz/` — the directory from which fz is run (project);
2. `~/.fz/` — the user's home (global, `--global` for `fz install`).

The project directory wins when both contain the same name.

```text
.fz/
├── models/          # <name>.json         -> model="name"
├── calculators/     # <name>.json (+ scripts)  -> calculators="name"
├── algorithms/      # <name>.py / <name>.R     -> algorithm="name"
└── tmp/             # per-run temporary directories (created by fz)
```

## Model alias

```json title=".fz/models/perfectgas.json"
{
  "id": "perfectgas",
  "delim": "{}",
  "output": {"pressure": "python://grep(r'pressure = (\\S+)', 'output.txt')"}
}
```

All fields: [Model Definition](../user-guide/models/definition.md). The file name is
the alias; `id` must be set for calculator aliases to match the model.

## Calculator alias

```json title=".fz/calculators/cluster.json"
{
  "uri": "ssh://user@hpc.example.edu",
  "models": {"perfectgas": "bash /home/user/codes/perfectgas/run.sh"},
  "code_id": "perfectgas@2.1"
}
```

Keys: `uri`, `models` (model `id` → command), `code_id`, `version_cmd`. See
[Calculators](../user-guide/calculators/overview.md#aliases). When `calculators` is
omitted, every alias supporting the model's `id` is used.

## Algorithms

`algorithm="brent"` loads `.fz/algorithms/brent.py` (or `.R`), then
`~/.fz/algorithms/`. Globs are accepted. See
[Writing Algorithms](../user-guide/design/algorithms.md).

## `.fz/tmp`

Each run creates temporary case directories under `./.fz/tmp/fz_temp_*` (and, for
`ssh://`, under `.fz/tmp/fz_calc_*` in the remote home). Their content is removed after
the run, but empty `fz_temp_*` directories remain and accumulate; `.fz/tmp/` can be
deleted when no run is active. Remote cleanup is restricted to fz's own directories.

## Inspecting

```bash
fz list --format json             # models and calculators (not algorithms)
ls .fz/algorithms ~/.fz/algorithms
```

## See also

[Environment Variables](environment.md) · [Installing Models & Algorithms](../user-guide/installing.md)
