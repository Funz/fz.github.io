# fzo - Parse Output Files

The `fzo` function reads and parses calculation results from output directories.

## Function Signature

```python
fz.fzo(output_dir, model)
```

## Parameters

- `output_dir` (str): Path to results directory
- `model` (dict): Model definition with output commands

## Returns

pandas DataFrame with results

## Example

```python
import fz

model = {
    "output": {
        "pressure": "grep 'Pressure:' output.txt | awk '{print $2}'"
    }
}

results = fz.fzo("results", model)
print(results)
```

## Output Command Forms

Each entry in `model["output"]` names a result column and says how to extract it. Since
**1.2**, several forms are available and can be freely mixed in one model:

| Form | Example | Requires |
|------|---------|----------|
| Shell command (implicit default, or `bash://`) | `"grep 'P:' out.txt \| awk '{print $2}'"` | bash + Unix tools |
| `python://` — native Python expression | `"python://grep(r'P: (\\S+)', 'out.txt')"` | nothing |
| `jq://` — JSON via a [jq](https://jqlang.org/) filter | `"jq://.energy results.json"` | `jq` on `PATH` |
| `yq://` — YAML/JSON/XML/TOML via [mikefarah/yq](https://github.com/mikefarah/yq) | `"yq://.metadata.version config.yaml"` | `yq` on `PATH` |
| `xpath://` — XML via `xmllint --xpath` | `"xpath://'//result/T/text()' out.xml"` | `xmllint` on `PATH` |
| Python callable (Python API only) | `lambda d: float((d / "final.txt").read_text())` | nothing |

The `python://` helpers available in expressions: `read(path)`, `lines(path)`,
`line(path, n)`, `grep(pattern, path, group=None, all=False, cast=True)`,
`json_file(path)`, `csv_file(path, column=None)`, `hdf5_file(path, dataset=None)` (needs
the optional `h5py` package), plus the modules `re`, `json`, `math`, `statistics`, `np`,
`pd`, and `Path`. Relative paths resolve against the case result directory. `grep`
returns the first capture group, cast to int/float when possible; `all=True` returns a
list of every match.

The shell-free forms (`python://`, `jq://`, `yq://`, `xpath://`) need no bash and are
fully portable on Windows.

### Vector (Array) Outputs

An output entry may resolve to a **list** rather than a scalar — a time series, a
spatial profile, a spectrum. `fzo` / `fzr` store the full list per case as-is, with no
flattening, truncation, or padding; different cases may have different lengths.

```python
model = {
    "output": {
        "T_series":  "python://csv_file('temps.csv', column='T')",
        "spectrum":  "jq://.spectrum results.json",
        "residuals": "python://grep(r'res=(\\S+)', 'log.txt', all=True)",
    }
}
```

!!! warning "Persisting vectors"
    `--format csv` / `to_csv()` stringifies lists (`"[1, 2, 3]"`). Use `--format json`,
    `to_pickle`, or `to_parquet` for a lossless round trip. The plain-shell / `bash://`
    form also unwraps a single-element array to a scalar — prefer `python://` / `jq://` /
    `yq://` / `xpath://` when a vector's length can legitimately be 1.

See the [main FZ documentation](https://github.com/Funz/fz) for complete details.
