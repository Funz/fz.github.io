# Troubleshooting

First read the failing case's `err.txt`, `log.txt` and `history.txt` (in its result
directory), and the `error` column of the DataFrame. For more detail:

```python
fz.set_log_level("DEBUG")        # or FZ_LOG_LEVEL=DEBUG before starting Python
```

## Symptoms and causes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `ValueError: results_dir looks like a calculator URI` (fz ≤ 1.2: a directory named `sh:/...` appears and every case fails) | Calculator passed as 4th positional argument of `fzr` (that slot is `results_dir`) | `calculators=...` by keyword |
| `Permission denied ... ./input.txt` | No calculator: fz fell back to an empty `sh://` | Give `calculators`, or install a calculator alias matching the model `id` |
| `fzi` misses `${x}` (fz ≤ 1.2) or `$(x)` variables | Model sets `delim` to the other pair (or fz ≤ 1.2 default `()`) | Fix `delim`, or remove it to accept both forms |
| `fzi` reports unexpected variables | `varprefix` collides with the code's syntax | Change `varprefix` (e.g. `%`) |
| Case `done` but output `None` and `error` = `Missing output: ...` | Extractor found nothing: wrong file/pattern, file written elsewhere, locale | Test the extractor with `fzo` on the case directory |
| Output value equals the program's stdout | The code writes `out.txt` (reserved, overwritten by stdout) | Rename the code's output file |
| Result file contains the input twice, or the command gets unexpected arguments | The compiled input names are appended to the end of the `sh://` command line | Move file handling into a script run as `sh://bash script.sh` |
| fz ≤ 1.2: result file in the launch directory, template read uncompiled | Old `sh://` path rewriting (fixed after 1.2, P0-8) | Upgrade; re-check results of such commands |
| fz ≤ 1.2: every case `timeout` immediately | `FZ_RUN_TIMEOUT=0` or `timeout=0` (now "no timeout") | Upgrade, or use model `"timeout": null` |
| `ssh://`/`slurm://` run never ends | No default timeout for these calculators | Set `FZ_RUN_TIMEOUT` or the model's `timeout` |
| Changing `os.environ["FZ_..."]` has no effect | Configuration is read at import | `fz.reload_config()` |
| `FZ_MAX_WORKERS=8` but cases still run one at a time | Parallelism = number of calculator entries | `calculators=["sh://bash calc.sh"] * 8` |
| `cache://results` with `results_dir="results"` never hits | The old directory was renamed before the lookup | Use `cache://_` |
| Cache hit although the code changed | The command/script is not part of the cache key | Declare `code_id` in calculator aliases, or use a fresh `results_dir` |
| `fzo results/` returns one row of `None` | `fzo` targets the directory itself | `fzo "results/*"` |
| After `fzc`, `compiled/input.txt` does not exist | `fzc` writes `compiled/<var=val,...>/input.txt` | Look into the case sub-directory |
| fz ≤ 1.2: `fz list --check` marks an installed calculator `failed` (`Empty sh:// command`) | Old `fz list` check of `{"uri": "sh://", "models": {...}}` aliases | Upgrade; check with a real `fzr` run |
| SSH run blocks at start | Host-key prompt (password in URI, unknown host) | Add the host to `known_hosts` or `FZ_SSH_AUTO_ACCEPT_HOSTKEYS=1` |
| `bash: not found` / shell errors on Windows | bash not found | Install MSYS2/Git Bash, set `FZ_SHELL_PATH` |
| `ValueError: signal only works in main thread` | fz < 1.2 called from a thread | Upgrade; since 1.2 the handler is skipped outside the main thread |
| R formulas unavailable although `rpy2` imports | `rpy2.robjects` fails to load (R/rpy2 version mismatch) | Align R and rpy2 versions |

## Verify step by step

```bash
fzi input.txt --model m --format json                        # variables found?
fzc input.txt --model m --input_variables '{"x": 1}' --output_dir compiled
(cd compiled/*/ && bash /abs/path/run.sh input.txt)          # code runs?
fzo 'compiled/*' --model m --format json                     # outputs parsed?
```

## See also

[Constraints & Limits](limitations.md) · [Environment Variables](environment.md)
