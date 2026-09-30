# fzd - Design of Experiments

`fzd` runs an iterative loop: an **algorithm** proposes a batch of points, fz evaluates
them (with `fzr` for a file-based model, or by calling a Python function), and the
algorithm uses the results to propose the next batch or stop. Use it for optimization,
calibration/inversion, adaptive sampling, uncertainty propagation.

| | `fzr` | `fzd` |
|--|-------|-------|
| Values | Given by you (grid or list) | Chosen by the algorithm within ranges |
| `input_variables` | `{"x": [1, 2, 3]}` | `{"x": "[0;10]", "y": "2.5"}` (strings) |
| Result | DataFrame | Dict with `XY` DataFrame, analysis, summary |

## Signature

```python
fz.fzd(
    input_path,               # template, or None for a Python function model
    input_variables,          # {"x": "[min;max]"} varied, {"z": "1.5"} fixed
    model,                    # model dict/alias, or a Python callable
    output_expression,        # "pressure", "a + 2*b", or a list for multi-objective
    algorithm,                # installed name, glob, or path to a .py/.R file
    calculators=None,
    algorithm_options=None,   # dict, JSON string or JSON file path
    analysis_dir="analysis",
    input_static=None,
) -> dict
```

| Parameter | Notes |
|-----------|-------|
| `input_variables` | `"[min;max]"` (or `"[min,max]"`) ranges are passed to the algorithm; plain value strings are fixed and merged into every point |
| `output_expression` | Evaluated on each case's outputs. A **list** of expressions gives a vector objective (multi-objective algorithms). May be `None` for a function model |
| `algorithm` | `"brent"` → `.fz/algorithms/brent.py` (then `~/.fz/algorithms/`), or a file path |
| `calculators` | File-based model: as in `fzr`; omitted → installed aliases matching the model `id`, else `sh://`. Function model: a positive int (concurrent evaluations, default 1) |
| `analysis_dir` | Output directory; an existing one is renamed with a timestamp and its results reused as cache |

## Result

| Key | Content |
|-----|---------|
| `XY` | DataFrame of all evaluated points: inputs and objective(s) |
| `analysis` | Processed output of the algorithm's `get_analysis()` (text, data, HTML/JSON file names) |
| `algorithm` | Algorithm used |
| `iterations` | Number of iterations |
| `total_evaluations` | Number of evaluated points |
| `summary` | e.g. `"randomsampling completed: 1 iterations, 5 evaluations (5 valid)"` |

`analysis_dir` contains `X_<i>.csv`, `Y_<i>.csv`, `results_<i>.html` (or `.json`/`.txt`
depending on the analysis content), one `iter<NNN>/` directory per iteration (cases
named `case_<i>`), and a campaign `manifest.json`.

## Example

```python
import fz

model = {
    "delim": "{}",
    "output": {"pressure": "python://grep(r'pressure = (\\S+)', 'output.txt')"},
}

result = fz.fzd(
    "input.txt",
    {"T_celsius": "[0;100]", "V_L": "[1;5]", "n_mol": "1"},
    model,
    output_expression="pressure",
    algorithm="examples/algorithms/montecarlo_uniform.py",   # path to the file
    calculators=["sh://bash calculate.sh"] * 4,              # 4 points at a time
    algorithm_options={"batch_sample_size": 20, "max_iterations": 10, "seed": 123},
    analysis_dir="mc_analysis",
)
print(result["summary"])
print(result["XY"].describe())
```

## Output expressions

Available names: the model outputs, `abs`, `min`, `max`, `pow`, `sqrt`, `exp`, `log`,
`log10`, `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`, `pi`, `e`, and for vector
outputs `sum`, `len`, `sorted`, `mean`, `median`, `stdev`, `variance`, `zip`, indexing
and slicing.

```python
output_expression = "r1 + 2 * r2"
output_expression = "T_series[-1]"                                      # last value
output_expression = "sqrt(sum((x - y)**2 for x, y in zip(sim, ref)) / len(sim))"  # RMSE
output_expression = ["f1", "-f2"]      # multi-objective: minimize f1, maximize f2
```

A vector output used without reduction makes that point fail (reported, non-fatal).
Multi-objective algorithms (e.g. `nsga2.py`) minimize every objective; negate an
expression to maximize it.

## Python function as model

With a callable model, no files and no calculators are involved:

```python
def branin(x, y):
    import math
    return (y - 5.1 / (4 * math.pi**2) * x**2 + 5 / math.pi * x - 6)**2 \
        + 10 * (1 - 1 / (8 * math.pi)) * math.cos(x) + 10

result = fz.fzd(None, {"x": "[-5;10]", "y": "[0;15]"}, branin,
                output_expression=None, algorithm="examples/algorithms/bfgs.py",
                calculators=1)
```

- `input_path` must be `None`; `input_variables` keys are the function's parameters.
- `output_expression=None` takes the return value (or its first item/key).
- `calculators=1` (default) calls the function sequentially in the calling thread.
  `calculators=N` uses N threads: the function must be thread-safe, and any error then
  aborts `fzd` with `fz.FunctionModelParallelError`.
- Each iteration directory contains only `values.csv`.

## Behaviors

- **Deduplication**: identical points within a batch are evaluated once.
- **Cross-iteration cache**: a point already evaluated is not re-run.
- **Re-run**: an existing `analysis_dir` is renamed with a timestamp and its iterations
  serve as cache for the new run.
- Iterations use `case_naming="index"` (`iter001/case_0/`), whatever `FZ_CASE_NAMING`.
- `input_static` is passed to every iteration's `fzr`.

## Algorithms

| Source | How to use |
|--------|------------|
| Examples shipped in the fz repository: `randomsampling.py`, `montecarlo_uniform.py`, `brent.py`, `bfgs.py`, `nsga2.py` ([examples/algorithms](https://github.com/Funz/fz/tree/main/examples/algorithms)) | Pass the file path, or copy it to `.fz/algorithms/` and use its name |
| Installable `fz-<name>` repositories (e.g. `fz-brent`, `fz-PSO`, `fz-gradientdescent`) | `fz install algorithm brent`, then `algorithm="brent"` |
| Your own | [Writing Algorithms](../design/algorithms.md) |

Each algorithm file lists its options and defaults in its `#options:` header.

## CLI

```bash
fzd --input_dir input.txt --model perfectgas \
    --input_vars '{"T_celsius": "[0;100]", "V_L": "[1;5]", "n_mol": "1"}' \
    --output_expression "pressure" \
    --algorithm examples/algorithms/montecarlo_uniform.py \
    --options '{"batch_sample_size": 20, "max_iterations": 10}' \
    --results_dir mc_analysis
```

- Also `fz design ...`. `--input_path`/`--input_variables`/`--variables` are accepted
  aliases of `--input_dir`/`--input_vars`.
- Differences with Python: the default directory is `results_fzd` (Python:
  `analysis`); `--output_expression` takes a single expression (no multi-objective
  list); there is no `--format` option (a summary is printed); function models are not
  available.

## See also

[Writing Algorithms](../design/algorithms.md) · [fzr](fzr.md) ·
[Installing Models & Algorithms](../installing.md) · [Caching](../running/caching.md)
