# Results & Traceability

## Layout

```text
results/                                  # results_dir (renamed with a timestamp if it exists)
├── manifest.json                         # campaign record
├── ro-crate-metadata.json                # same, as RO-Crate 1.1 (FZ_RO_CRATE=0 disables)
├── cases.csv                             # only with case_naming "hash" / "index"
├── T=10,P=1/                             # one directory per case
│   ├── input.txt                         # compiled inputs
│   ├── output.txt ...                    # files written by the code
│   ├── out.txt   err.txt                 # stdout / stderr of the command
│   ├── log.txt                           # command, exit code, times, user, host, platform
│   ├── info.txt                          # state, calculator, inputs, outputs (key=value)
│   ├── history.txt                       # timeline of the case (attempts, errors)
│   └── .fz_hash                          # cache key (SHA-256 of inputs, code_id)
└── ...
```

!!! warning "Reserved names"
    `out.txt`, `err.txt`, `log.txt`, `info.txt`, `history.txt`, `.fz_hash` are written by
    fz in every case directory and overwrite files of the same name produced by the
    code. `manifest.json`, `ro-crate-metadata.json`, `cases.csv` are reserved at the
    results root.

When the template has no variables (single non-parametric run), the files are written
directly in `results_dir`.

## Case directory naming

`case_naming` (argument, `--case_naming`, or `FZ_CASE_NAMING`):

| Value | Example | Notes |
|-------|---------|-------|
| `"path"` (default) | `T=10,P=1,V=a%2Fb` | Readable. Characters `/ \ : * ? " < > \| %` and control characters are percent-encoded; `.`/`..` values are encoded. Can exceed the ~255-character name limit with many variables or long values |
| `"hash"` | `case_c39cc51bad10` | Short hash of the variable combination; stable across runs |
| `"index"` | `case_0` | Position in the design |

With `"hash"`/`"index"`, `cases.csv` maps each directory to its variables
(`case,T,P,...`). The values are also in each case's `info.txt` (`input.T=10`), which
`fzo` reads when a directory name cannot be parsed. `fzd` always uses `"index"`.

fz refuses to create a case directory that would resolve outside `results_dir`.

## Campaign manifest

`manifest.json` is written at the end of every `fzr` (and, per campaign, by `fzd` in
`analysis_dir`, linking the iteration manifests):

| Key | Content |
|-----|---------|
| `schema` | `fz-manifest/1` |
| `fz_version`, `python_version`, `platform`, `dependencies` | Software environment |
| `start_time`, `end_time` | UTC timestamps |
| `interrupted` | Whether Ctrl+C was pressed |
| `input_path`, `model`, `model_sha256` | What was run |
| `calculators`, `hosts` | Where (passwords in URIs masked) |
| `n_cases`, `n_done` | Counts |
| `cases` | Per case: `path`, `status`, `calculator`, `inputs`, `.fz_hash` SHA-256, `code_id` when known |

`ro-crate-metadata.json` describes the same campaign as an
[RO-Crate](https://www.researchobject.org/ro-crate/) (`Dataset`, `File`,
`SoftwareApplication`, `CreateAction`). Failure to write either file logs a warning and
never fails the run.

## Shared static files (`input_static`)

Files identical for every case (a large mesh, a weather series, a cross-section
library) should not be in `input_path`: they would be copied into every case and
re-hashed each time. Pass them with `input_static` (`fzi`, `fzc`, `fzr`, `fzd`; CLI
`--input_static`, repeatable or a JSON list):

```python
fz.fzr("input.txt", variables, model,
       calculators="sh://bash calc.sh",
       input_static=["reference_data.csv", "/shared/big_mesh.msh"])
```

| Entry | Behavior |
|-------|----------|
| Relative path | Resolved against the current directory, identified by its base name, symlinked into each case (copied where symlinks are not allowed), uploaded to `ssh://`, remote `slurm://` and `funz://` calculators |
| Absolute path | Must exist at the same path on the calculator (shared storage); never copied or transferred, only hashed |

Static files are never templated and are excluded from `fzi`. They are hashed once per
call and included in `.fz_hash`, so the cache reacts to their content. `fzr` warns once
per file when a variable-free `input_path` file is at least
`FZ_STATIC_CANDIDATE_MIN_SIZE` bytes (default 1 MiB; `0` disables).

## Reading results later

```python
import pandas as pd, json
df = fz.fzo("results/*", model)                   # re-parse, possibly with a new model
manifest = json.load(open("results/manifest.json"))
```

## See also

[fzr](../core-functions/fzr.md) · [Caching](caching.md) ·
[Output Extraction](../models/outputs.md)
