# Core Concepts

Understanding these fundamental concepts will help you use FZ effectively.

## The FZ Workflow

FZ follows a simple four-step workflow:

```mermaid
graph LR
    A[Input Template] -->|fzi| B[Parse Variables]
    B -->|fzc| C[Compile Cases]
    C -->|Calculator| D[Execute]
    D -->|fzo| E[Parse Results]
    
    style A fill:#e1f5fe
    style E fill:#c8e6c9
```

1. **Parse** - Identify variables in input templates
2. **Compile** - Substitute values and evaluate formulas
3. **Execute** - Run calculations
4. **Parse** - Extract results

The `fzr` function orchestrates all four steps automatically.

## Variables

Variables are placeholders in input templates that get replaced with actual values.

### Variable Syntax

```text
temperature = $temp
pressure = $press
concentration = $conc
```

The `$` prefix marks a variable (customizable via `varprefix`).

### Variable Types

FZ supports scalar and list values:

```python
# Scalar variable (single value)
{"temperature": 100}

# List variable (multiple values)
{"temperature": [100, 200, 300]}

# Mixed
{
    "temperature": [100, 200, 300],  # 3 cases
    "pressure": 1.0                   # Fixed
}
```

## Parametric Studies

When you provide lists of values, FZ creates the **Cartesian product**:

```python
input_variables = {
    "temp": [10, 20],      # 2 values
    "volume": [1, 2, 3],   # 3 values
    "amount": 1.0          # Fixed
}
# Creates 2 × 3 = 6 cases:
# temp=10, volume=1, amount=1.0
# temp=10, volume=2, amount=1.0
# temp=10, volume=3, amount=1.0
# temp=20, volume=1, amount=1.0
# temp=20, volume=2, amount=1.0
# temp=20, volume=3, amount=1.0
```

## Formulas

Formulas are evaluated during compilation to create calculated values.

### Formula Syntax

```text
# Simple formula
result = @($a + $b)

# With functions
#@ def square(x):
#@     return x * x
area = @(square($width))

# Multi-line
#@ import math
#@ radius = $diameter / 2
#@ area = math.pi * radius**2
circle_area = @(area)
```

### Formula Features

- **Python or R** expressions (set with `FZ_INTERPRETER` env var)
- **Variable substitution** - Use variables with `$` in formulas
- **Function definitions** - Define reusable functions
- **Context sharing** - Variables defined in one formula available in others

## Models

A model defines how to parse inputs and extract outputs.

### Basic Model

```python
model = {
    "varprefix": "$",
    "output": {
        "result": "cat output.txt"
    }
}
```

### Complete Model

```python
model = {
    # Input parsing
    "varprefix": "$",           # Variable marker
    "formulaprefix": "@",       # Formula marker
    "delim": "()",              # Formula delimiters
    "commentline": "#",         # Comment lines
    
    # Output extraction
    "output": {
        "pressure": "grep 'P:' out.txt | awk '{print $2}'",
        "temp": "grep 'T:' out.txt | awk '{print $2}'",
        "energy": "python extract_energy.py"
    },
    
    # Optional identifier
    "id": "mymodel"
}
```

### Model Aliases

Store models in `.fz/models/mymodel.json` and use by name:

```python
results = fz.fzr("input.txt", variables, "mymodel")
```

## Calculators

Calculators define **where** and **how** calculations are executed.

### Calculator Types

| Type | URI Format | Purpose |
|------|------------|---------|
| **Shell** | `sh://command args` | Local execution |
| **SSH** | `ssh://user@host/command` | Remote execution |
| **Cache** | `cache://directory` | Reuse previous results |

### Calculator Examples

```python
# Local shell
calculators = "sh://bash script.sh"

# Remote SSH
calculators = "ssh://user@server.com/bash /path/to/script.sh"

# Cache with fallback
calculators = [
    "cache://previous_results",
    "sh://bash script.sh"
]
```

### Multiple Calculators

Provide a list for parallel execution or failover:

```python
# Parallel execution (4 workers)
calculators = [
    "sh://bash calc.sh",
    "sh://bash calc.sh",
    "sh://bash calc.sh",
    "sh://bash calc.sh"
]

# Failover chain
calculators = [
    "cache://results",              # Try cache first
    "sh://bash fast_method.sh",     # Fast but unstable
    "sh://bash robust_method.sh",   # Slow but reliable
    "ssh://user@hpc/bash calc.sh"   # Remote fallback
]
```

## Results Structure

FZ organizes results in a clear directory structure:

```
results/
├── T_celsius=10,V_L=1/
│   ├── input.txt          # Compiled input
│   ├── output.txt         # Calculation output
│   ├── log.txt            # Execution metadata
│   ├── out.txt            # Standard output
│   ├── err.txt            # Standard error
│   └── .fz_hash           # Input file hashes
├── T_celsius=10,V_L=2/
│   └── ...
└── T_celsius=20,V_L=1/
    └── ...
```

### DataFrame Output

Results are returned as a pandas DataFrame:

```python
   T_celsius  V_L  n_mol  pressure  status  calculator  error  command
0       10.0  1.0    1.0   2353.58    done      sh://   None   bash...
1       10.0  2.0    1.0   1176.79    done      sh://   None   bash...
2       20.0  1.0    1.0   2437.30    done      sh://   None   bash...
```

Columns include:

- **Input variables** - All parameters
- **Output variables** - Extracted results
- **Metadata** - Status, calculator used, errors, command

## Caching

FZ uses MD5 hashes of input files for intelligent caching.

### How Caching Works

1. **Hash Generation** - MD5 hash of all input files stored in `.fz_hash`
2. **Cache Check** - Compare hash with cached results
3. **Reuse** - If match found and outputs valid, reuse results
4. **Fallback** - If no match, proceed to next calculator

### Cache Strategy

```python
# First run
results1 = fz.fzr(
    "input.txt",
    {"param": [1, 2, 3]},
    model,
    calculators="sh://expensive_calc.sh",
    results_dir="run1"
)

# Add more cases - reuse previous
results2 = fz.fzr(
    "input.txt",
    {"param": [1, 2, 3, 4, 5]},  # 2 new cases
    model,
    calculators=[
        "cache://run1",              # Reuse 1, 2, 3
        "sh://expensive_calc.sh"     # Calculate 4, 5
    ],
    results_dir="run2"
)
```

## Parallel Execution

FZ automatically parallelizes when multiple calculators are available.

### How It Works

1. **Round-robin distribution** - Cases distributed to calculators
2. **Thread-safe locking** - Each calculator locked during execution
3. **Load balancing** - Available calculators pick up new cases
4. **Progress tracking** - ETA calculated based on completed cases

### Controlling Parallelism

```python
# Environment variable
import os
os.environ['FZ_MAX_WORKERS'] = '8'

# Or duplicate calculators
calculators = ["sh://bash calc.sh"] * 8
```

## Error Handling

FZ provides robust error handling and retry mechanisms.

### Retry Strategy

```python
import os
os.environ['FZ_MAX_RETRIES'] = '3'

results = fz.fzr(
    "input.txt",
    variables,
    model,
    calculators=[
        "sh://unreliable.sh",
        "sh://backup.sh"
    ]
)
```

Process:
1. Try first calculator
2. On failure, try next calculator
3. Repeat up to `MAX_RETRIES` times
4. Report final status in DataFrame

### Graceful Interrupts

Press Ctrl+C to stop gracefully:

- First Ctrl+C: Complete current calculations, save partial results
- Second Ctrl+C: Force quit (not recommended)

Resume with cache:

```python
results = fz.fzr(
    "input.txt",
    variables,
    model,
    calculators=[
        "cache://interrupted_run",
        "sh://bash calc.sh"
    ]
)
```

## Configuration

FZ can be configured via:

### Environment Variables

```bash
export FZ_LOG_LEVEL=DEBUG
export FZ_MAX_RETRIES=5
export FZ_MAX_WORKERS=4
export FZ_INTERPRETER=python
```

### Configuration Files

Store models and calculators in `.fz/`:

```
.fz/
├── models/
│   ├── model1.json
│   └── model2.json
└── calculators/
    ├── cluster1.json
    └── cluster2.json
```

### Python API

```python
from fz import get_config

config = get_config()
config.max_retries = 10
config.max_workers = 8
```

## Best Practices

### 1. Start Small

Test with a few cases first:

```python
# Development
results = fz.fzr("input.txt", {"param": [1, 2]}, model, ...)

# Production
results = fz.fzr("input.txt", {"param": range(1000)}, model, ...)
```

### 2. Use Caching

Always include cache in calculator chain:

```python
calculators = [
    "cache://previous_results",
    "sh://bash calc.sh"
]
```

### 3. Handle Failures

Check status column:

```python
failed = results[results['status'] != 'done']
if len(failed) > 0:
    print(f"Failed cases: {len(failed)}")
    print(failed[['status', 'error']])
```

### 4. Organize Results

Use descriptive directory names:

```python
results_dir = f"results_{model_name}_{timestamp}"
```

### 5. Document Models

Include comments in model definitions:

```json
{
    "varprefix": "$",
    "output": {
        "pressure": "grep 'P:' output.txt | awk '{print $2}'  # Extract pressure in Pa"
    }
}
```

## Next Steps

Now that you understand the core concepts:

- [Core Functions](../user-guide/core-functions/fzi.md) - Deep dive into fzi, fzc, fzo, fzr
- [Model Definition](../user-guide/model-definition.md) - Advanced model configuration
- [Calculators](../user-guide/calculators/overview.md) - Master calculator types
- [Examples](../examples/perfectgas.md) - See concepts in action
