# Environment Variables

The variables of the General, Execution, Cache and SSH tables are read **once, when
`fz` is imported**: set them before starting Python, or call `fz.reload_config()` after
changing `os.environ`. `fz.print_config()` shows the effective values. SLURM array
variables are read when the first `slurm-array://` case is submitted, MCP variables when
`fz-mcp` starts.

## General

| Variable | Default | Meaning |
|----------|---------|---------|
| `FZ_LOG_LEVEL` | `ERROR` | `QUIET`, `ERROR`, `WARNING`, `INFO`, `DEBUG`. Logs go to stderr |
| `FZ_INTERPRETER` | `python` | Default formula interpreter (`python` or `R`); a model's `interpreter` wins |
| `FZ_SHELL_PATH` | unset | Directories searched first for `bash` and the commands of shell calculators/extractors (`;`-separated on Windows, `:` elsewhere). Needed on Windows (MSYS2/Git Bash) |

## Execution

| Variable | Default | Meaning |
|----------|---------|---------|
| `FZ_MAX_WORKERS` | unset | Upper bound on concurrent cases; never above the number of non-cache calculator entries (except `slurm-array://`) |
| `FZ_MAX_RETRIES` | `5` | Calculator failures tolerated per case before `failed` |
| `FZ_RUN_TIMEOUT` | `3600` for `sh://`/`funz://`, none for `ssh://`/`slurm://` | Per-case timeout in seconds; when set, applies to all calculators; `0` = no timeout ([Timeouts](../user-guide/running/timeouts.md)) |
| `FZ_CASE_NAMING` | `path` | Case directory naming: `path`, `hash`, `index` (invalid values fall back to `path`) |
| `FZ_STATIC_CANDIDATE_MIN_SIZE` | `1048576` | Size (bytes) above which a variable-free input file triggers the `input_static` suggestion; `0` disables |
| `FZ_RO_CRATE` | `1` | `0` disables `ro-crate-metadata.json` (`manifest.json` is always written) |

## Cache

| Variable | Default | Meaning |
|----------|---------|---------|
| `FZ_CACHE_STRICT` | `0` | `1` refuses cache matches whose code identity cannot be verified |
| `FZ_CACHE_ACCEPT_LEGACY` | `0` | `1` lets `cache://` use caches written in the old MD5 format |

## SSH

| Variable | Default | Meaning |
|----------|---------|---------|
| `FZ_SSH_KEEPALIVE` | `300` | Keepalive interval (s) |
| `FZ_SSH_AUTO_ACCEPT_HOSTKEYS` | `0` | `1` accepts unknown host keys without prompting (the prompt only occurs with a password in the URI; key authentication already adds unknown hosts) |
| `SSH_USER` | local user | User name when the URI has no `user@` (read at connection time) |

## SLURM job arrays

| Variable | Default | Meaning |
|----------|---------|---------|
| `FZ_SLURM_ARRAY_WINDOW` | `1` | Seconds during which cases are gathered into one `sbatch --array` |
| `FZ_SLURM_POLL_INTERVAL` | `2` | Seconds between `sacct`/`squeue` polls |

## MCP server

| Variable | Default | Meaning |
|----------|---------|---------|
| `FZ_MCP_ROOT` | working directory | Root to which all file paths are confined |
| `FZ_MCP_TRUSTED` | `1` | `0`: models/calculators must be installed aliases |
| `FZ_MCP_TRANSPORT` | `stdio` | `sse` or `streamable-http` (requires the next variable) |
| `FZ_MCP_ALLOW_NETWORK_TRANSPORT` | `0` | `1` allows a network transport |

## Examples

=== "Linux / macOS"

    ```bash
    export FZ_LOG_LEVEL=INFO FZ_MAX_WORKERS=8 FZ_RUN_TIMEOUT=7200
    python run_study.py
    ```

=== "Windows (PowerShell)"

    ```powershell
    $env:FZ_SHELL_PATH = "C:\msys64\usr\bin;C:\msys64\mingw64\bin"
    python run_study.py
    ```

=== "Python"

    ```python
    import os, fz
    os.environ["FZ_MAX_RETRIES"] = "3"
    fz.reload_config()
    fz.set_log_level("DEBUG")          # or directly, without environment variables
    fz.get_config().max_workers = 4
    ```

## See also

[.fz Directory & Aliases](configuration.md) · [Constraints & Limits](limitations.md)
