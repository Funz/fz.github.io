# Troubleshooting

## Common Issues

**Calculations fail with "command not found"**

Use absolute paths in calculator URIs:

```bash
calculators = "sh://bash /full/path/to/script.sh"
```

**SSH calculations hang**

Increase timeout or verify SSH connectivity:

```bash
# Test manually
ssh user@host "bash script.sh"
```

**Cache not working**

Check `.fz_hash` files exist in cache directories. Enable debug logging:

```python
import os
os.environ['FZ_LOG_LEVEL'] = 'DEBUG'
```

**Out of memory with many parallel cases**

Limit parallel workers:

```bash
export FZ_MAX_WORKERS=2
```

## Windows / Cross-Platform

**Shell commands fail on Windows**

Install MSYS2 and set `FZ_SHELL_PATH` to point to its binaries:

```powershell
$env:FZ_SHELL_PATH = "C:\msys64\usr\bin;C:\msys64\mingw64\bin"
```

See [FZ_SHELL_PATH configuration](https://github.com/Funz/fz/blob/main/examples/shell_path_example.md) for details.

**Line ending issues on Windows**

Write input files with Unix line endings:

```python
with open("input.txt", "w", newline='\n') as f:
    f.write(content)
```

**`chmod` has no effect on Windows**

This is expected — Windows does not support Unix file permissions. Shell scripts run via `sh://` do not need `chmod` on Windows.

## Debug Mode

Enable detailed logging:

```python
import os
os.environ['FZ_LOG_LEVEL'] = 'DEBUG'

results = fz.fzr(...)  # Will show detailed execution logs
```

Debug output includes:

- Calculator selection and locking
- File operations and command execution
- Cache matching
- Thread pool management

See the [main FZ documentation](https://github.com/Funz/fz#troubleshooting) for more details.
