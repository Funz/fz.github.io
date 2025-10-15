# fzr - Run Parametric Study

The `fzr` function orchestrates complete parametric studies by combining all FZ capabilities: parsing inputs, compiling cases, executing calculations, and collecting results.

## Function Signature

```python
fz.fzr(
    input_path,
    input_variables,
    model,
    calculators,
    results_dir="results",
    **kwargs
)
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `input_path` | `str` | Yes | Path to input file or directory |
| `input_variables` | `dict` | Yes | Dictionary of variable names and values |
| `model` | `dict` or `str` | Yes | Model definition or model alias name |
| `calculators` | `str` or `list` | Yes | Calculator URI(s) |
| `results_dir` | `str` | No | Output directory (default: "results") |

## Returns

**pandas.DataFrame** - Results with columns for:

- All input variables
- All output variables defined in model
- Metadata: `status`, `calculator`, `error`, `command`

## Basic Usage

### Simple Parametric Study

```python
import fz

model = {
    "varprefix": "$",
    "output": {
        "result": "cat output.txt"
    }
}

results = fz.fzr(
    input_path="input.txt",
    input_variables={"temperature": [100, 200, 300]},
    model=model,
    calculators="sh://bash calculate.sh",
    results_dir="results"
)

print(results)
```

### Full Factorial Design

```python
results = fz.fzr(
    "input.txt",
    {
        "pressure": [1, 10, 100],      # 3 values
        "temperature": [300, 400, 500], # 3 values
        "concentration": 0.5            # Fixed
    },  # Total: 3 × 3 = 9 cases
    model,
    calculators="sh://bash calc.sh"
)
```

## Variable Handling

### Scalar Variables

Fixed values for all cases:

```python
results = fz.fzr(
    "input.txt",
    {
        "param1": 100,        # Fixed
        "param2": "value",    # Fixed string
        "param3": [1, 2, 3]   # Variable
    },
    model,
    calculators="sh://bash calc.sh"
)
# Creates 3 cases
```

### List Variables

Creates Cartesian product:

```python
results = fz.fzr(
    "input.txt",
    {
        "x": [1, 2],       # 2 values
        "y": [10, 20, 30]  # 3 values
    },
    model,
    calculators="sh://bash calc.sh"
)
# Creates 2 × 3 = 6 cases
```

### Large Parameter Spaces

```python
import numpy as np

results = fz.fzr(
    "input.txt",
    {
        "param1": np.linspace(0, 10, 50),    # 50 values
        "param2": np.logspace(-3, 3, 20),    # 20 values
        "param3": [0.1, 0.5, 1.0]            # 3 values
    },  # Total: 50 × 20 × 3 = 3000 cases
    model,
    calculators=["sh://bash calc.sh"] * 8  # 8 parallel workers
)
```

## Calculator Options

### Single Calculator

```python
results = fz.fzr(
    "input.txt",
    variables,
    model,
    calculators="sh://bash calculate.sh"
)
```

### Multiple Calculators (Parallel)

```python
results = fz.fzr(
    "input.txt",
    variables,
    model,
    calculators=[
        "sh://bash calc.sh",
        "sh://bash calc.sh",
        "sh://bash calc.sh",
        "sh://bash calc.sh"
    ]  # 4 parallel workers
)
```

### Failover Chain

```python
results = fz.fzr(
    "input.txt",
    variables,
    model,
    calculators=[
        "cache://previous_results",        # Try cache
        "sh://bash fast_method.sh",        # Fast method
        "sh://bash robust_method.sh",      # Backup
        "ssh://user@hpc/bash remote.sh"    # Remote fallback
    ]
)
```

### Remote Execution

```python
results = fz.fzr(
    "input.txt",
    variables,
    model,
    calculators="ssh://user@server.com/bash /path/to/calculate.sh"
)
```

## Model Options

### Dictionary Model

```python
model = {
    "varprefix": "$",
    "formulaprefix": "@",
    "delim": "()",
    "commentline": "#",
    "output": {
        "pressure": "grep 'P:' output.txt | awk '{print $2}'",
        "temperature": "grep 'T:' output.txt | awk '{print $2}'"
    }
}

results = fz.fzr("input.txt", variables, model, calculators)
```

### Model Alias

Save model to `.fz/models/mymodel.json`:

```json
{
    "varprefix": "$",
    "output": {
        "result": "cat output.txt"
    }
}
```

Use by name:

```python
results = fz.fzr("input.txt", variables, "mymodel", calculators)
```

## Results Analysis

### Basic Analysis

```python
results = fz.fzr(...)

# Summary statistics
print(results.describe())

# Check for failures
failed = results[results['status'] != 'done']
print(f"Failed: {len(failed)}")

# Group by variable
grouped = results.groupby('temperature').agg({
    'pressure': ['mean', 'std', 'min', 'max']
})
print(grouped)
```

### Filtering Results

```python
# Filter by condition
high_pressure = results[results['pressure'] > 1000]

# Filter by multiple conditions
subset = results[
    (results['temperature'] > 300) &
    (results['pressure'] < 2000)
]

# Filter by status
successful = results[results['status'] == 'done']
```

### Visualization

```python
import matplotlib.pyplot as plt

# Line plot
for temp in results['temperature'].unique():
    data = results[results['temperature'] == temp]
    plt.plot(data['pressure'], data['result'], label=f'T={temp}')
plt.legend()
plt.show()

# Scatter plot
plt.scatter(results['temperature'], results['pressure'], 
            c=results['result'], cmap='viridis')
plt.colorbar(label='Result')
plt.show()
```

## Advanced Features

### Parallel Execution Control

```python
import os

# Set maximum workers
os.environ['FZ_MAX_WORKERS'] = '16'

results = fz.fzr(
    "input.txt",
    large_variables,
    model,
    calculators=["sh://bash calc.sh"] * 16
)
```

### Retry Configuration

```python
import os

# Set retry limit
os.environ['FZ_MAX_RETRIES'] = '5'

results = fz.fzr(
    "input.txt",
    variables,
    model,
    calculators=[
        "sh://unreliable_method.sh",
        "sh://backup_method.sh"
    ]
)
```

### Interrupt Handling

```python
try:
    results = fz.fzr(
        "input.txt",
        {"param": list(range(1000))},
        model,
        calculators="sh://bash slow_calc.sh"
    )
except KeyboardInterrupt:
    print("Interrupted! Partial results saved.")
    # Resume with cache
    results = fz.fzr(
        "input.txt",
        {"param": list(range(1000))},
        model,
        calculators=[
            "cache://results",
            "sh://bash slow_calc.sh"
        ],
        results_dir="results_resumed"
    )
```

### Caching Strategy

```python
# First run
results1 = fz.fzr(
    "input.txt",
    {"param": [1, 2, 3, 4, 5]},
    model,
    calculators="sh://bash expensive.sh",
    results_dir="run1"
)

# Extend with caching
results2 = fz.fzr(
    "input.txt",
    {"param": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
    model,
    calculators=[
        "cache://run1",              # Reuse 1-5
        "sh://bash expensive.sh"     # Calculate 6-10
    ],
    results_dir="run2"
)
```

## Output Directory Structure

```
results/
├── param=1/
│   ├── input.txt          # Compiled input
│   ├── output.txt         # Calculation output
│   ├── log.txt            # Execution metadata
│   ├── out.txt            # Standard output
│   ├── err.txt            # Standard error
│   └── .fz_hash           # File checksums
├── param=2/
│   └── ...
└── param=3/
    └── ...
```

## Complete Examples

### Example 1: Sensitivity Analysis

```python
import fz
import numpy as np

model = {
    "varprefix": "$",
    "output": {
        "result": "grep 'Result:' output.txt | awk '{print $2}'"
    }
}

# Vary one parameter at a time
baseline = {"A": 1.0, "B": 2.0, "C": 3.0}

for param in ['A', 'B', 'C']:
    variables = baseline.copy()
    variables[param] = np.linspace(0.5, 1.5, 20)
    
    results = fz.fzr(
        "model.txt",
        variables,
        model,
        calculators="sh://bash simulate.sh",
        results_dir=f"sensitivity_{param}"
    )
    
    print(f"Sensitivity to {param}:")
    print(results[[param, 'result']].corr())
```

### Example 2: Design of Experiments

```python
import fz
from itertools import combinations

model = {
    "varprefix": "$",
    "output": {"response": "cat response.txt"}
}

# Full factorial
variables = {
    "factor1": [-1, 0, 1],
    "factor2": [-1, 0, 1],
    "factor3": [-1, 0, 1]
}

results = fz.fzr(
    "experiment.txt",
    variables,
    model,
    calculators="sh://bash run_experiment.sh",
    results_dir="doe_results"
)

# Analyze main effects
for factor in ['factor1', 'factor2', 'factor3']:
    effect = results.groupby(factor)['response'].mean()
    print(f"\n{factor} effect:")
    print(effect)

# Analyze interactions
for f1, f2 in combinations(['factor1', 'factor2', 'factor3'], 2):
    interaction = results.groupby([f1, f2])['response'].mean()
    print(f"\n{f1} × {f2} interaction:")
    print(interaction)
```

### Example 3: Optimization Search

```python
import fz
import numpy as np

model = {
    "varprefix": "$",
    "output": {"objective": "cat objective.txt"}
}

# Initial grid search
results = fz.fzr(
    "optimize.txt",
    {
        "x": np.linspace(-10, 10, 20),
        "y": np.linspace(-10, 10, 20)
    },
    model,
    calculators="sh://bash evaluate.sh",
    results_dir="grid_search"
)

# Find best region
best = results.loc[results['objective'].idxmin()]
print(f"Best found: x={best['x']}, y={best['y']}, obj={best['objective']}")

# Refine search around optimum
results2 = fz.fzr(
    "optimize.txt",
    {
        "x": np.linspace(best['x']-1, best['x']+1, 20),
        "y": np.linspace(best['y']-1, best['y']+1, 20)
    },
    model,
    calculators=[
        "cache://grid_search",
        "sh://bash evaluate.sh"
    ],
    results_dir="refined_search"
)
```

## Error Handling

```python
import fz

try:
    results = fz.fzr(
        "input.txt",
        variables,
        model,
        calculators="sh://bash calc.sh"
    )
except FileNotFoundError:
    print("Input file not found")
except ValueError as e:
    print(f"Invalid configuration: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")

# Check results
if 'status' in results.columns:
    failures = results[results['status'] != 'done']
    if len(failures) > 0:
        print(f"\nFailed cases: {len(failures)}")
        print(failures[['status', 'error']])
```

## Performance Tips

1. **Use caching** for expensive calculations
2. **Parallelize** with multiple calculators
3. **Batch similar cases** for better locality
4. **Filter early** to reduce data processing
5. **Save checkpoints** for long runs

## See Also

- [fzi](fzi.md) - Parse input variables
- [fzc](fzc.md) - Compile input files
- [fzo](fzo.md) - Parse output files
- [Calculators](../calculators/overview.md) - Calculator types
- [Parallel Execution](../advanced/parallel.md) - Parallelization guide
