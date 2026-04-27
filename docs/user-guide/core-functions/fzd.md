# fzd - Design of Experiments

The `fzd` function (or `fz design` command) runs iterative design of experiments with adaptive algorithms. Unlike `fzr` which runs a fixed grid of parameter combinations, `fzd` lets algorithms intelligently choose which points to evaluate next based on previous results.

## When to Use fzd vs fzr

| Feature | `fzr` | `fzd` |
|---------|-------|-------|
| **Parameter values** | You specify exact values | Algorithm chooses from ranges |
| **Design type** | Fixed factorial/custom grid | Adaptive, iterative |
| **Use case** | Parameter sweeps, sensitivity analysis | Optimization, uncertainty quantification |
| **Input format** | `{"x": [1, 2, 3]}` (values) | `{"x": "[0;10]"}` (ranges) |

## Python API

### Function Signature

```python
import fz

result = fz.fzd(
    input_path,
    input_variables,
    model,
    output_expression,
    algorithm,
    calculators=None,
    algorithm_options=None,
    analysis_dir="analysis"
)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `input_path` | `str` | Path to input file or directory |
| `input_variables` | `dict` | Variable ranges: `{"var": "[min;max]"}` or fixed: `{"var": "value"}` |
| `model` | `dict` or `str` | Model definition or alias |
| `output_expression` | `str` | Expression to evaluate (e.g., `"pressure"` or `"r1 + r2 * 2"`) |
| `algorithm` | `str` | Path to algorithm Python file |
| `calculators` | `str` or `list` | Calculator URI(s) (default: `["sh://"]`) |
| `algorithm_options` | `dict`, `str`, or `None` | Algorithm options as dict, JSON string, or JSON file path |
| `analysis_dir` | `str` | Analysis results directory (default: `"analysis"`) |

### Return Value

Returns a dictionary with:

| Key | Type | Description |
|-----|------|-------------|
| `XY` | `DataFrame` | All sampled input/output values |
| `analysis` | varies | Algorithm analysis results (HTML, plots, metrics) |
| `algorithm` | `str` | Algorithm file path used |
| `iterations` | `int` | Number of algorithm iterations completed |
| `total_evaluations` | `int` | Total number of function evaluations |
| `summary` | `str` | Human-readable summary text |

## CLI Usage

### Command Signature

```bash
fzd --input_dir DIR --input_vars VARS --model MODEL \
    --output_expression EXPR --algorithm ALGO \
    [--results_dir DIR] [--calculators CALC] [--options OPTS]
```

Or using the main `fz` command:

```bash
fz design --input_dir DIR --input_vars VARS --model MODEL \
    --output_expression EXPR --algorithm ALGO [...]
```

### CLI Options

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--input_dir` | `-i` | Yes | Input directory path |
| `--input_vars` | `-v` | Yes | Variable ranges (JSON file or inline JSON) |
| `--model` | `-m` | Yes | Model definition (JSON file, inline JSON, or alias) |
| `--output_expression` | `-e` | Yes | Output expression to optimize |
| `--algorithm` | `-a` | Yes | Algorithm name (`randomsampling`, `brent`, `bfgs`, ...) or file path |
| `--results_dir` | `-r` | No | Results directory (default: `results_fzd`) |
| `--calculators` | `-c` | No | Calculator specifications |
| `--options` | `-o` | No | Algorithm options (JSON file or inline JSON) |

## Examples

### Example 1: Random Sampling

Explore the parameter space with random sampling:

```python
import fz

model = {
    "varprefix": "$",
    "delim": "()",
    "run": "bash -c 'source input.txt && result=$(echo \"scale=6; $x * $x + $y * $y\" | bc) && echo \"result = $result\" > output.txt'",
    "output": {
        "result": "grep 'result = ' output.txt | cut -d '=' -f2 | tr -d ' '"
    }
}

result = fz.fzd(
    input_path="input/",
    input_variables={"x": "[-2;2]", "y": "[-2;2]"},
    model=model,
    output_expression="result",
    algorithm="examples/algorithms/randomsampling.py",
    algorithm_options={"nvalues": 20, "seed": 42}
)

print(f"Total evaluations: {result['total_evaluations']}")
df = result['XY']
best = df.loc[df['result'].idxmin()]
print(f"Best: x={best['x']:.4f}, y={best['y']:.4f}, result={best['result']:.6f}")
```

### Example 2: 1D Optimization (Brent's Method)

Find the minimum of a 1D function:

```python
result = fz.fzd(
    input_path="input/",
    input_variables={"x": "[0;2]"},
    model=model_1d,
    output_expression="result",
    algorithm="examples/algorithms/brent.py",
    algorithm_options={"max_iter": 20, "tol": 1e-3}
)

df = result['XY']
best = df.loc[df['result'].idxmin()]
print(f"Optimal x = {best['x']:.6f} (expected: 0.7)")
```

### Example 3: Multi-dimensional Optimization (BFGS)

Find the minimum of a multi-dimensional function with parallel evaluations:

```python
result = fz.fzd(
    input_path="input/",
    input_variables={"x": "[-2;2]", "y": "[-2;2]"},
    model=model,
    output_expression="result",
    algorithm="examples/algorithms/bfgs.py",
    algorithm_options={"max_iter": 20, "tol": 1e-4},
    calculators=["sh://bash calc.sh"] * 4  # 4 parallel evaluators
)
```

### Example 4: Monte Carlo with Convergence

Run Monte Carlo sampling until a confidence interval target is reached:

```python
result = fz.fzd(
    input_path="input.txt",
    input_variables={
        "n_mol": "[0;10]",
        "T_celsius": "[0;100]",
        "V_L": "[1;5]"
    },
    model=perfectgas_model,
    output_expression="pressure + 1",
    algorithm="examples/algorithms/montecarlo_uniform.py",
    calculators=["sh://bash PerfectGazPressure.sh"] * 10,
    algorithm_options={
        "batch_sample_size": 20,
        "max_iterations": 50,
        "confidence": 0.90,
        "target_confidence_range": 1000000,
        "seed": 123
    },
    analysis_dir="fzd_analysis"
)
```

### Example 5: Custom Output Expression

Combine multiple model outputs in an expression:

```python
result = fz.fzd(
    input_path="input/",
    input_variables={"x": "[-2;2]", "y": "[-2;2]"},
    model=model_multi_output,
    output_expression="r1 + r2 * 2",  # Custom expression
    algorithm="examples/algorithms/randomsampling.py",
    algorithm_options={"nvalues": 20, "seed": 42}
)
```

Available expression operators: `+`, `-`, `*`, `/`, `**`, `abs()`, `min()`, `max()`, `sqrt()`, `exp()`, `log()`, `pi`, `e`.

### Example 6: CLI Usage

```bash
# Random sampling
fzd -i input/ -m perfectgas \
  -v '{"x": "[-2;2]", "y": "[-2;2]"}' \
  -e "result" \
  -a examples/algorithms/randomsampling.py \
  -o '{"nvalues": 20, "seed": 42}'

# Algorithm options from a JSON file
fzd -i input/ -m perfectgas \
  -v '{"x": "[-2;2]"}' \
  -e "result" \
  -a examples/algorithms/brent.py \
  -o algo_config.json \
  -r optimization_results/

# As fz subcommand
fz design -i input/ -m perfectgas \
  -v '{"x": "[-2;2]", "y": "[-2;2]"}' \
  -e "result" \
  -a examples/algorithms/bfgs.py
```

## Algorithm Options Formats

Algorithm options can be provided in three formats:

=== "Dict (Python API)"

    ```python
    algorithm_options={"batch_size": 20, "max_iterations": 10, "seed": 42}
    ```

=== "JSON String (CLI)"

    ```bash
    --options '{"batch_size": 20, "max_iterations": 10, "seed": 42}'
    ```

=== "JSON File"

    ```bash
    --options algo_config.json
    ```

## Input Variables: Ranges vs Fixed Values

`input_variables` accepts two kinds of entries:

| Format | Example | Behaviour |
|--------|---------|-----------|
| Range | `"[min;max]"` or `"[min,max]"` | Handed to the algorithm; it decides which values to sample |
| Fixed | `"5.0"` (a plain number string) | Constant — merged into every design point unchanged, never varied |

```python
# x and y are explored; z is fixed at 1.5 for every evaluation
result = fz.fzd(
    input_path="input/",
    input_variables={"x": "[-2;2]", "y": "[-2;2]", "z": "1.5"},
    ...
)
```

## Automatic Behaviors

### Batch Deduplication

Within each iteration, duplicate design points proposed by the algorithm are evaluated only once. The results are re-mapped so the algorithm receives the correct output for every point it requested, including duplicates. This prevents redundant expensive evaluations when an algorithm proposes the same point twice.

### Cross-Iteration Caching

Results from previous iterations are automatically reused — a point evaluated in iteration 2 is never re-run in iteration 5. No extra configuration is required.

### Re-Run Resume

If `analysis_dir` already exists when `fzd` starts, it is **renamed** with a timestamp suffix (e.g., `analysis_2026-04-27_10-30-00`) and the original path is used for the new run. The renamed directory's iteration subdirectories are still added to the cache, so a re-run with different algorithm options benefits from all prior computations automatically.

```python
# Re-run after an interrupted or exploratory first run — prior results reused as cache
result = fz.fzd(
    input_path="input/",
    input_variables={"x": "[-2;2]"},
    algorithm="examples/algorithms/bfgs.py",
    analysis_dir="my_analysis"   # if exists → renamed; its cache still consulted
)
```

## Available Algorithms

FZ ships with example algorithms in `examples/algorithms/`:

| Algorithm | File | Type | Best For |
|-----------|------|------|----------|
| Random Sampling | `randomsampling.py` | Exploration | Initial exploration, baselines |
| Brent's Method | `brent.py` | 1D optimization | Precise 1D root finding/optimization |
| BFGS | `bfgs.py` | Multi-D optimization | Smooth multi-dimensional optimization |
| Monte Carlo | `montecarlo_uniform.py` | Integration | Uncertainty quantification |

!!! tip "Choosing an Algorithm"
    - **1D problems**: Use Brent's method
    - **2-10D smooth problems**: Use BFGS
    - **Exploratory / non-smooth**: Use random sampling
    - **Uncertainty quantification**: Use Monte Carlo

## Writing Custom Algorithms

Custom algorithms must implement a Python class with the following interface:

```python
class MyAlgorithm:

    def __init__(self, options):
        """Initialize with algorithm-specific options dict."""
        self.batch_size = int(options.get("batch_size", 10))

    def get_initial_design(self, input_variables, output_variables):
        """Return initial list of sample points.

        Args:
            input_variables: dict of {"var_name": "[min;max]"} ranges
            output_variables: list of output variable names

        Returns:
            List of dicts, each dict is one sample point:
            [{"x": 1.0, "y": 2.0}, {"x": 3.0, "y": 4.0}, ...]
        """
        pass

    def get_next_design(self, X, Y):
        """Return next sample points or None to stop.

        Args:
            X: list of input dicts evaluated so far
            Y: list of output values evaluated so far

        Returns:
            List of dicts for next batch, or None to stop iteration.
        """
        pass

    def get_analysis(self, X, Y):
        """Return analysis results (called at end).

        Args:
            X: all input dicts
            Y: all output values

        Returns:
            HTML string, dict, or any serializable result.
        """
        pass
```

### Algorithm File Header

Algorithm files should include metadata in comments:

```python
#title: My Algorithm Name
#author: Author Name
#type: sampling|optimization
#options: batch_size=10;max_iterations=100;seed=42
#require: numpy;scipy
```

## See Also

- [fzr](fzr.md) - Run fixed parametric studies
- [fzi](fzi.md) - Parse input variables
- [fzl](fzl.md) - List available models/calculators
- [Algorithm Options Example](https://github.com/Funz/fz/blob/main/examples/algorithm_options_example.md)
- [FZD Examples](https://github.com/Funz/fz/blob/main/examples/fzd_example.md)
