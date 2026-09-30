# Output Extraction

The model's `output` field maps each result **column name** to an **extractor**. After a
case has run, every extractor is evaluated **inside the case's result directory**, and
its value becomes the column's value for that case. The same extractors are used by
`fzo` on existing directories.

## Extractor forms

Forms can be mixed within one model.

| Form | Example | Requires |
|------|---------|----------|
| Shell command (default, or `bash://` prefix) | `"grep 'P:' output.txt \| awk '{print $2}'"` | bash and the tools used |
| `python://` expression | `"python://grep(r'P: (\\S+)', 'output.txt')"` | nothing |
| `jq://filter file` | `"jq://.energy results.json"` | `jq` |
| `yq://filter file` | `"yq://.metadata.version config.yaml"` | [mikefarah/yq](https://github.com/mikefarah/yq) |
| `xpath://expr file` | `"xpath://'//result/T/text()' out.xml"` | `xmllint` |
| Python callable (Python API only) | `lambda d: float((d / "final.txt").read_text())` | nothing |

`python://`, `jq://`, `yq://` and `xpath://` do not use bash and work on Windows without
MSYS2. A callable receives the case directory as a `pathlib.Path`.

### `python://` helpers

Relative paths are resolved against the case directory.

| Helper | Returns |
|--------|---------|
| `read(path)` | File content as a string |
| `lines(path)` | List of lines |
| `line(path, n)` | Line `n` |
| `grep(pattern, path, group=None, all=False, cast=True)` | First capture group (or whole match) of the first match, cast to int/float when possible; `all=True` returns the list of all matches |
| `json_file(path)` | Parsed JSON |
| `csv_file(path, column=None)` | A column as a list, or the table |
| `hdf5_file(path, dataset=None)` | A dataset (needs `h5py`) |

Also available in expressions: `re`, `json`, `math`, `statistics`, `np`, `pd`, `Path`,
`base_dir`.

```python
model = {
    "delim": "{}",
    "output": {
        "pressure":  "python://grep(r'pressure = (\\S+)', 'output.txt')",
        "T_max":     "python://max(csv_file('temps.csv', column='T'))",
        "residuals": "python://grep(r'res=(\\S+)', 'solver.log', all=True)",
        "energy":    "jq://.energy results.json",
    },
}
```

## Value conversion

The text produced by a shell/`jq`/`yq`/`xpath` extractor is converted, in this order:
JSON (`[1, 2]`, `{"a": 1}`), Python literal, `int`/`float`, otherwise kept as a string.
An empty result gives `None`.

| Extractor output | Value |
|------------------|-------|
| `1.5` | `1.5` |
| `[1, 2, 3]` | `[1, 2, 3]` |
| `[7]` from a **shell** command | `7` (single-element lists are unwrapped) |
| `[7]` from `python://`/`jq://`/`yq://`/`xpath://` | `[7]` (kept as a list) |
| `{"min": 1, "max": 4}` | expanded by `fzr` into columns `name_min`, `name_max` |
| *(empty)* | `None` |

## Vector outputs

An extractor may return a list (time series, profile, spectrum). `fzr` and `fzo` store
the whole list in the cell, without flattening or padding; cases may have different
lengths. `fzd` needs a scalar objective: reduce vectors in `output_expression`
(`mean(T_series)`, `T_series[-1]`, ... see [fzd](../core-functions/fzd.md)).

!!! warning "Persisting vectors"
    CSV turns lists into strings (`"[1, 2, 3]"`). Use `--format json`, `to_pickle()` or
    `to_parquet()` to keep them as lists.

## Failures

When an extractor fails (missing file, empty output), the value is `None` and:

- `fzo` adds a column `_output_error` with the reason;
- `fzr` keeps the case `status` and writes `Missing output: <reason>` in the `error`
  column.

A `cache://` hit is only accepted when all outputs, re-parsed with the current model,
are non-`None`.

## Pitfalls

- **Reserved file names.** Do not parse results from `out.txt`, `err.txt`, `log.txt`,
  `info.txt` or `history.txt` unless you mean fz's own files: `out.txt` *is* the
  captured stdout of the command, which is a valid source when the code prints its
  results.
- **Locale.** Shell tools may use a comma decimal separator. Prefix numeric pipelines
  with `LC_ALL=C`, or use `python://`.
- **`python` vs `python3`.** Shell extractors calling `python` use whatever is first on
  `PATH`.
- **Quoting awk fields.** In JSON files write `$3` normally; inside a single-quoted
  inline `--model '...'` it is safe; never inside double quotes on the shell command
  line.

## See also

- [Model Definition](definition.md)
- [fzo](../core-functions/fzo.md)
- [Results & Traceability](../running/results.md)
