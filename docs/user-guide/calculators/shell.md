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

## File names in the command line

- A bare word naming a file (`calculate.sh`, `data.txt`) is made absolute in the
  **launch directory** only if it exists there **and not** in the case directory: a
  helper script next to your Python script works (`sh://bash calculate.sh`), while the
  compiled inputs of the case always win. Targets of `>`, `>>`, `2>` are never rewritten.
  Each rewritten word is logged at INFO level; the `command` column shows the result.
- The compiled input file names are appended to the end of the **whole** command line,
  after pipes and redirections: `sh://cat input.txt > res.txt` runs
  `cat input.txt > res.txt input.txt`, so `res.txt` contains the input twice.

!!! note "Before this fix (fz ≤ 1.2)"
    Every file-looking word was rewritten to the launch directory, even when absent:
    `sh://cat input.txt > res.txt` read the **uncompiled template** and wrote `res.txt`
    outside the case, without error. Results obtained with such commands should be
    re-checked.

**Rule:** put the work in a script and launch it with `sh://bash script.sh`. Inside the
script, relative paths are the case directory, and `$1`, `$2`, ... are the compiled
input files.

```bash title="calculate.sh"
#!/bin/bash
# runs in the case directory; $1 = compiled input file
source "$1"
./solver --in "$1" --out result.dat > solver.log 2>&1 || exit 1
```

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
