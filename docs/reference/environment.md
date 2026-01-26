# Environment Variables

FZ can be configured using several environment variables to customize its behavior.

## Core Configuration

### `FZ_LOG_LEVEL`
**Description**: Controls the verbosity of FZ logging output.

**Values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

**Default**: `INFO`

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

### `FZ_EXECUTION_TIMEOUT`
**Description**: Default timeout in seconds for calculator execution. Can be overridden by model configuration or calculator URI parameters.

**Values**: Positive integer (seconds)

**Default**: `None` (no timeout)

**Example**:
```bash
export FZ_EXECUTION_TIMEOUT=300  # 5 minutes
```

### `FZ_MAX_RETRIES`
**Description**: Maximum number of retry attempts when a calculator fails.

**Values**: Non-negative integer

**Default**: `3`

**Example**:
```bash
export FZ_MAX_RETRIES=5
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

## SSH Configuration

### `FZ_SSH_KEEPALIVE`
**Description**: Interval in seconds for SSH keepalive packets to prevent connection timeout.

**Values**: Positive integer (seconds)

**Default**: `60`

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

