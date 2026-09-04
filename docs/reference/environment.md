# Environment Variables

FZ can be configured using several environment variables to customize its behavior.

## Core Configuration

### `FZ_LOG_LEVEL`
**Description**: Controls the verbosity of FZ logging output.

**Values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

**Default**: `ERROR`

**Example**:
```bash
export FZ_LOG_LEVEL=DEBUG
```

### `FZ_INTERPRETER`
**Description**: Default formula interpreter for evaluating expressions.

**Values**: `python`, `R`

**Default**: `python`

**Example**:
```bash
export FZ_INTERPRETER=R
```

## Execution Configuration

### `FZ_RUN_TIMEOUT` (renamed in 1.2, default raised to 1 h)

**Description**: Default timeout in seconds for a single case run. A model can override
it with its own `"timeout"` entry (`None`/`null`/`0` disables the timeout for that
model); an explicit `timeout=` argument to `fzr()` / `fzc()` overrides both.

**Values**: Positive integer (seconds), or `0` to disable

**Default**: `3600` (1 hour — was `600` before 1.2)

**Example**:
```bash
export FZ_RUN_TIMEOUT=300  # 5 minutes
```

!!! note
    Earlier releases named this variable `FZ_EXECUTION_TIMEOUT`. Use `FZ_RUN_TIMEOUT`.

### `FZ_MAX_RETRIES`
**Description**: Maximum number of retry attempts when a calculator fails.

**Values**: Non-negative integer

**Default**: `5`

**Example**:
```bash
export FZ_MAX_RETRIES=3
```

### `FZ_MAX_WORKERS`
**Description**: Maximum number of parallel workers for concurrent execution.

**Values**: Positive integer

**Default**: Number of CPU cores

**Example**:
```bash
export FZ_MAX_WORKERS=8
```

## Shell Configuration

### `FZ_SHELL_PATH` (New in 0.9.1)
**Description**: Custom search path for shell commands and executables. Overrides system PATH for binary resolution. Essential for Windows users with MSYS2, Git Bash, or custom tool locations.

**Format**: 
- Windows: Semicolon-separated paths
- Unix/Linux: Colon-separated paths

**Default**: System PATH

**Example**:
```bash
# Windows
SET FZ_SHELL_PATH=C:\msys64\usr\bin;C:\msys64\mingw64\bin;C:\Python39

# Linux/macOS
export FZ_SHELL_PATH=/opt/tools/bin:/usr/local/bin
```

**Features**:
- Automatic `.exe` extension handling on Windows
- Binary path caching for performance
- Overrides system PATH priority

## Case Layout Configuration

### `FZ_CASE_NAMING` (New in 1.2)
**Description**: How each case's result/temp subdirectory is named. `"path"` produces
`var1=val1,var2=val2,...` (human-readable, but can exceed the ~255-char filename limit
with many variables); `"hash"` uses a short content hash of the variable combination;
`"index"` uses `case_<i>`. With `"hash"` / `"index"` a `cases.csv` manifest mapping each
directory to its variables is written at the results root. Overridden by the
`case_naming=` argument / `--case_naming` flag.

**Values**: `path`, `hash`, `index`

**Default**: `path`

**Example**:
```bash
export FZ_CASE_NAMING=hash
```

### `FZ_STATIC_CANDIDATE_MIN_SIZE` (New in 1.2)
**Description**: Size threshold in bytes above which an `input_path` file with no
variables triggers a one-time warning suggesting it be passed via `input_static`
instead (it is otherwise re-read, re-copied, and re-hashed on every case). Set to `0`
to disable the warning.

**Values**: Non-negative integer (bytes)

**Default**: `1048576` (1 MiB)

**Example**:
```bash
export FZ_STATIC_CANDIDATE_MIN_SIZE=0
```

## SSH Configuration

### `FZ_SSH_KEEPALIVE`
**Description**: Interval in seconds for SSH keepalive packets to prevent connection timeout.

**Values**: Positive integer (seconds)

**Default**: `300`

**Example**:
```bash
export FZ_SSH_KEEPALIVE=30
```

## Cache Configuration

### `FZ_CACHE_DIR`
**Description**: Directory for storing cached results.

**Values**: Valid directory path

**Default**: `.fz/cache` in working directory

**Example**:
```bash
export FZ_CACHE_DIR=/tmp/fz_cache
```

## Discovery Configuration

### `FZ_UDP_DISCOVERY_PORT`
**Description**: UDP port for Funz calculator auto-discovery.

**Values**: Valid port number

**Default**: `21001`

**Example**:
```bash
export FZ_UDP_DISCOVERY_PORT=21001
```

## Configuration Files

### Model and Calculator Aliases

FZ looks for configuration files in:

- **Models**: `~/.fz/models/` and `./.fz/models/`
- **Calculators**: `~/.fz/calculators/` and `./.fz/calculators/`

Configuration files use JSON format:

**Model Example** (`~/.fz/models/perfectgas.json`):
```json
{
  "varprefix": "$",
  "interpreter": "python",
  "output": {
    "pressure": "grep 'P =' output.txt | awk '{print $3}'"
  }
}
```

**Calculator Example** (`~/.fz/calculators/compute.json`):
```json
{
  "uri": "ssh://user@cluster.example.edu/bash",
  "models": ["perfectgas", "simulation"]
}
```

## Platform-Specific Notes

### Windows

- Use `SET` instead of `export` for environment variables
- Path separators are semicolons (`;`) in `FZ_SHELL_PATH`
- Consider setting `FZ_SHELL_PATH` for Git Bash or MSYS2 tools

### Linux/macOS

- Use `export` for environment variables
- Path separators are colons (`:`) in `FZ_SHELL_PATH`
- Environment variables can be set in `~/.bashrc` or `~/.zshrc`

## See Also

- [Configuration Guide](configuration.md) - Model and calculator configuration
- [Shell Calculator](../user-guide/calculators/shell.md) - Shell execution details
- [Troubleshooting](troubleshooting.md) - Common issues and solutions

