# Local Shell (`sh://`)

`sh://` runs the case on the local machine, through bash, in a temporary directory
created for the case.

```text
sh://command [arguments]
```

```python
calculators = "sh://bash calculate.sh"
calculators = "sh://python3 simulate.py --verbose"
calculators = ["sh://bash calculate.sh"] * 4        # 4 cases at a time
```

## Execution of one case

1. The compiled input files (and `input_static` files) are placed in a temporary
   directory under `.fz/tmp/`.
2. The command runs **in that directory**, with the input file names appended to the
   end of the command line: `bash /abs/path/calculate.sh input.txt`.
3. stdout → `out.txt`, stderr → `err.txt`.
4. Files are copied to the case result directory and the outputs are parsed there.

Exit status 0 means the run succeeded; the case is then `done` if outputs can be
parsed. A non-zero status is a failure and the case is retried.

## Path rewriting in the command line

!!! warning "Relative file names are resolved against the launch directory"
    Before running, every token of the command that looks like a file name
    (`calculate.sh`, `data/mesh.msh`, `result.txt`) is made **absolute relative to the
    directory from which `fzr` was called**, not the case directory. Common tools
    (`bash`, `sh`, `python`, `python3`, `cat`, `cp`, `mv`, `rm`, `grep`, `awk`, `sed`,
    ...), flags (`-x`, `--opt=v`) and numbers are left unchanged.

    `sh://cat input.txt > res.txt` therefore reads the **uncompiled template** of the
    launch directory and writes `res.txt` outside the case; the case ends `done` with
    empty outputs.

**Rule:** put the work in a script and launch it with `sh://bash script.sh`. Inside the
script, relative paths are the case directory, and `$1`, `$2`, ... are the compiled
input files.

```bash title="calculate.sh"
#!/bin/bash
# runs in the case directory; $1 = compiled input file
source "$1"
./solver --in "$1" --out result.dat > solver.log 2>&1 || exit 1
```

The rewritten command is logged at INFO level and stored in the `command` column.

## Windows

`sh://` needs bash (MSYS2 or Git Bash). Set `FZ_SHELL_PATH` to their `bin` directories
before starting Python; commands found there are resolved to absolute paths. See
[Environment Variables](../../reference/environment.md#general).

## Timeout and interrupts

Default timeout 3600 s ([Timeouts](../running/timeouts.md)). On Ctrl+C the process is
terminated (then killed after 5 s) and the case is `interrupted`.

## See also

[SSH](ssh.md) · [SLURM](slurm.md) · [Calculators overview](overview.md) ·
[Constraints & Limits](../../reference/limitations.md)
