# Calculators

A calculator says **where and how** one case runs. It is given as a URI string, an alias
name, a dict, or a list of these, in the `calculators` argument of `fzr` / `fzd`.

## Types

| URI | Runs | Default timeout | Page |
|-----|------|-----------------|------|
| `sh://command` | Local shell, in a temporary directory per case | 3600 s | [Local shell](shell.md) |
| `ssh://[user[:pw]@]host[:port]/command` | Remote host; files transferred by SFTP | none | [SSH](ssh.md) |
| `slurm://[user@host[:port]]:partition/command` | `srun` on a SLURM partition, local or through SSH | none | [SLURM](slurm.md) |
| `slurm-array://:partition/command` | Local SLURM; all cases batched in one job array | none | [SLURM](slurm.md#job-arrays-slurm-array) |
| `funz://[host]:udp_port/code` | Java Funz calculator, found by UDP discovery | 3600 s | [Funz](funz.md) |
| `cache://path` | Nothing: reuses results of previous runs | — | [Cache](cache.md) |

## Several calculators

A list serves two purposes at once:

- **Parallelism**: each non-cache entry runs one case at a time, so N entries run up to
  N cases concurrently (`["sh://bash calc.sh"] * 4`).
- **Failover**: a case whose run fails is retried on the calculators, up to
  `FZ_MAX_RETRIES` (default 5) failures.

```python
calculators = [
    "cache://previous_run",                    # reused when inputs match
    "sh://bash calc.sh",                       # local
    "sh://bash calc.sh",                       # 2nd local slot
    "ssh://user@node1/bash /opt/code/run.sh",  # remote slot
]
```

Case *i* first tries entry *i mod n*, then the first free one. See
[Parallelism & Retries](../running/parallel.md).

## Default when `calculators` is omitted

`fzr` and `fzd` look for aliases in `.fz/calculators/` supporting the model's `id`; if
none is found they use `sh://` with no command, which fails (it tries to execute the
input file: `Permission denied ... ./input.txt`).

## Aliases

An alias is a JSON file in `./.fz/calculators/` (then `~/.fz/calculators/`), used by its
file name without `.json`.

```json title=".fz/calculators/cluster.json"
{
  "uri": "ssh://user@hpc.example.edu",
  "models": {
    "perfectgas": "bash /home/user/codes/perfectgas/run.sh",
    "cfd":        "bash /home/user/codes/cfd/run.sh"
  },
  "code_id": "perfectgas@2.1"
}
```

```python
fz.fzr("input.txt", variables, "perfectgas", calculators="cluster")
# runs: ssh://user@hpc.example.edu/bash /home/user/codes/perfectgas/run.sh
```

| Key | Role |
|-----|------|
| `uri` | Scheme and location; may contain the command directly (`"sh://bash run.sh"`) |
| `models` | Model `id` → command on that calculator. Only models listed here are run on it |
| `code_id` | Identity of the installed code, used by `cache://` to decide whether results of another calculator are reusable ([Caching](../running/caching.md#cache-identity-code_id)) |
| `version_cmd` | Command whose output gives the `code_id` (run once per calculator per session) |

The model must carry the same `id` for the `models` map to apply. `calculators` also
accepts a glob or regex on alias names (`"local*"`, `"^hpc"`) and a path to a JSON file.

Installed wrappers ship an alias `localhost_<Code>.json` of the form
`{"uri": "sh://", "models": {"<Code>": "bash .fz/calculators/<Code>.sh"}}`.

## Rules common to all calculators

- The command receives the **compiled input file names appended to its command line**.
- stdout/stderr of the command are saved as `out.txt` / `err.txt` in the case directory;
  `log.txt`, `info.txt`, `history.txt`, `.fz_hash` are also written by fz. A code
  writing results under one of these names loses them.
- A password in a URI is masked in results, logs and manifests, but prefer SSH keys.
- Calculator commands are executed as written: only use aliases you trust
  ([Security](../../reference/security.md)).

## See also

[Parallelism & Retries](../running/parallel.md) · [Timeouts](../running/timeouts.md) ·
[.fz Directory & Aliases](../../reference/configuration.md)
