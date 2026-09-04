# Local Shell Calculator (`sh://`)

The `sh://` calculator runs your computational code locally, in a shell, in a private
temporary directory per case. It is the default calculator and the one used in most
examples.

## URI Syntax

```
sh://command [arguments]
```

The command is whatever you would type to run one case by hand — a script, an
interpreter plus a script, or a compiled binary:

```python
calculators = "sh://bash calculate.sh"
calculators = "sh://python3 simulate.py --verbose"
calculators = "sh://./run_simulation"
calculators = "sh://bash run.sh --method=fast --tolerance=1e-6"
```

## How It Works

1. FZ creates a unique temporary directory for the case.
2. All compiled input files (and any [`input_static`](../core-functions/fzr.md#shared-static-files-new-in-12) files) are copied/linked in.
3. The command runs in that directory, receiving the input file name(s) as arguments:
   ```bash
   bash calculate.sh input.txt          # single input file
   bash calculate.sh file1.txt cfg.ini  # multiple input files
   ```
4. Outputs are extracted with the model's [`output`](../model-definition.md#output-extraction-updated-in-12) specs.
5. The temp directory is removed (kept when `FZ_LOG_LEVEL=DEBUG`).

## Example Calculator Script

```bash title="calculate.sh"
#!/bin/bash
INPUT_FILE=$1

# Read input variables written by the compiled template
source "$INPUT_FILE"

echo "Running with temp=$temp, pressure=$pressure"
result=$(echo "scale=2; $temp * $pressure / 100" | bc)

echo "result=$result" > output.txt
```

```python
model = {
    "varprefix": "$",
    "output": {"result": "grep 'result=' output.txt | cut -d= -f2"},
}

results = fz.fzr(
    "input.txt",
    {"temp": [100, 200, 300], "pressure": [1, 10]},
    model,
    calculators="sh://bash calculate.sh",
)
```

## Parallel Execution

Each calculator entry handles one case at a time. Pass several to run cases concurrently:

```python
calculators = ["sh://bash calc.sh"] * 4   # 4 workers
```

See [Parallel Execution](../advanced/parallel.md) for details.

## Windows

`sh://` needs a POSIX shell and the usual Unix utilities. Install MSYS2 or Git Bash and
point [`FZ_SHELL_PATH`](../../reference/environment.md#fz_shell_path-new-in-091) at their
`bin` directories. Since 1.2, `import fz` itself works without bash — only `sh://` and
`bash://` outputs require it; the [`python://` / `jq://` / `yq://` / `xpath://`](../core-functions/fzo.md#output-command-forms)
output forms do not.

## See Also

- [SSH Remote Calculator](ssh.md) · [SLURM](slurm.md) · [Funz Server](funz.md) · [Cache](cache.md)
- [Calculators Overview](overview.md)
- [Environment Variables](../../reference/environment.md)
