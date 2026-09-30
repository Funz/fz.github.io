# Quick Start

This page runs a complete study: the pressure of a perfect gas, `P = nRT/V`, for 4
temperatures × 3 volumes = 12 cases. Every file below is complete; the output shown was
produced by running them.

## 1. Input template

A template is the code's normal input file with `$variables` and `@{formulas}`.

```text title="input.txt"
# Perfect gas: n_mol, T_celsius, V_L are variables
n_mol=$n_mol
T_kelvin=@{$T_celsius + 273.15}
#@ def L_to_m3(L):
#@     return L / 1000
V_m3=@{L_to_m3($V_L)}
```

- `$n_mol`, `$T_celsius`, `$V_L`: variables, replaced by a value in each case.
- `@{...}`: formulas, evaluated in Python when the case is compiled.
- `#@` lines: code made available to formulas (here a function).

## 2. Calculation script

The "simulation" reads the compiled input and writes a result file.

```bash title="calculate.sh"
#!/bin/bash
# $1 is the compiled input file, in the case directory
source "$1"
P=$(python3 -c "print($n_mol * 8.314 * $T_kelvin / $V_m3)")
echo "pressure = $P" > output.txt
```

fz runs the script inside a fresh directory per case and appends the compiled input
file names to the command line, so `$1` is `input.txt`.

!!! warning "Do not name result files `out.txt`, `err.txt`, `log.txt`, `info.txt`, `history.txt`"
    fz writes these files in every case directory (stdout, stderr, metadata) and would
    overwrite a result file of the same name.

## 3. Model and run

```python title="run_study.py"
import fz

model = {
    "varprefix": "$",       # these four values are the defaults
    "formulaprefix": "@",
    "delim": "{}",
    "commentline": "#",
    "output": {
        "pressure": "python://grep(r'pressure = (\\S+)', 'output.txt')",
    },
}

results = fz.fzr(
    "input.txt",
    {"T_celsius": [10, 20, 30, 40], "V_L": [1, 2, 5], "n_mol": 1.0},  # 4 x 3 = 12 cases
    model,
    calculators=["sh://bash calculate.sh"] * 2,   # 2 cases at a time
    results_dir="results",
)
print(results[["T_celsius", "V_L", "n_mol", "pressure", "status"]].head())
```

```text title="output"
   T_celsius  V_L  n_mol    pressure status
0         10    1    1.0  2354109.10   done
1         10    2    1.0  1177054.55   done
2         10    5    1.0   470821.82   done
3         20    1    1.0  2437249.10   done
4         20    2    1.0  1218624.55   done
```

!!! danger "Pass `calculators=` and `results_dir=` by keyword"
    The 4th positional parameter of `fz.fzr` is `results_dir`, not `calculators`.
    `fz.fzr("input.txt", vars, model, "sh://bash calculate.sh")` creates a directory
    named `sh:/bash calculate.sh` and runs without calculator: every case fails.

## 4. What was produced

```text
results/
├── manifest.json                     # campaign record (versions, model, calculators, cases)
├── ro-crate-metadata.json            # same, as RO-Crate metadata
├── T_celsius=10,V_L=1,n_mol=1.0/
│   ├── input.txt                     # compiled input
│   ├── output.txt                    # written by calculate.sh
│   ├── out.txt  err.txt              # stdout / stderr of the command
│   ├── log.txt  info.txt  history.txt
│   └── .fz_hash                      # SHA-256 of the inputs (cache key)
└── ...                               # 11 more case directories
```

The returned DataFrame has one row per case: the variables, the outputs, and
`status`, `calculator`, `error`, `command`. A case whose `status` is not `done` has its
diagnosis in that case's `err.txt` and `log.txt`.

## 5. The same from the command line

```bash
fzr input.txt \
    --model '{"output": {"pressure": "python://grep(r\"pressure = (\\S+)\", \"output.txt\")"}}' \
    --input_variables '{"T_celsius": [10, 20, 30, 40], "V_L": [1, 2, 5], "n_mol": 1.0}' \
    --calculators "sh://bash calculate.sh" \
    --results_dir results --format json
```

Data goes to stdout, logs and progress to stderr; the exit status is 1 when no case
succeeds.

## 6. Check each step before a large run

For a new code, verify the steps separately; each one isolates a class of errors.

```python
fz.fzi("input.txt", model)
# {'T_celsius': None, 'V_L': None, 'n_mol': None,
#  'T_celsius + 273.15': None, 'L_to_m3(V_L)': None}   variables and formulas found

fz.fzc("input.txt", {"T_celsius": 10, "V_L": 1, "n_mol": 1.0}, model, "compiled")
# compiled/T_celsius=10,V_L=1,n_mol=1.0/input.txt        one sub-directory per case
#   T_kelvin=283.15, V_m3=0.001                          compilation correct?
```

```bash
(cd compiled/*/ && bash ../../calculate.sh input.txt)       # does the code run?
```

```python
fz.fzo("compiled/*", model)                                # does parsing find the value?
# path=compiled/T_celsius=10,V_L=1,n_mol=1.0, pressure=2354109.1, T_celsius=10, ...
```

`fzo` must target the case directory (or a glob of case directories): `fz.fzo("compiled",
model)` looks for `output.txt` in `compiled/` itself and returns `None`.

## 7. Next steps

- Reuse finished cases: add `"cache://results"` first in `calculators`
  ([Caching](../user-guide/running/caching.md)).
- Run elsewhere: [SSH](../user-guide/calculators/ssh.md),
  [SLURM](../user-guide/calculators/slurm.md).
- Let an algorithm choose the points (optimization, sampling):
  [fzd](../user-guide/core-functions/fzd.md).

    ```python
    fz.fzd("input.txt",
           {"T_celsius": "[0;100]", "V_L": "[1;5]", "n_mol": "1"},   # ranges, fixed values
           model,
           output_expression="pressure",
           algorithm="randomsampling",          # .fz/algorithms/randomsampling.py
           calculators="sh://bash calculate.sh",
           algorithm_options={"nvalues": 5})
    # summary: "randomsampling completed: 1 iterations, 5 evaluations (5 valid)"
    ```

    `randomsampling.py` is copied from fz's
    [`examples/algorithms/`](https://github.com/Funz/fz/tree/main/examples/algorithms);
    `algorithm=` also accepts a path to a `.py`/`.R` file.

- Read the [Constraints & Limits](../reference/limitations.md) before wrapping a real code.
