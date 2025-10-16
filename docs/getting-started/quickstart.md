# Quick Start

This guide will get you up and running with FZ in just a few minutes. We'll create a simple parametric study for the ideal gas law.

## The Complete Example

We'll calculate pressure for different temperatures and volumes using the ideal gas law: `PV = nRT`

### Step 1: Create Input Template

Create a file named `input.txt`:

```text
# input file for Perfect Gas Pressure, with variables n_mol, T_celsius, V_L
n_mol=$n_mol
T_kelvin=@($T_celsius + 273.15)
#@ def L_to_m3(L):
#@     return(L / 1000)
V_m3=@(L_to_m3($V_L))
```

**What's happening here?**

- `$n_mol`, `$T_celsius`, `$V_L` are **variables** (marked with `$`)
- `@(...)` are **formulas** that are evaluated during compilation
- `#@` lines define Python functions available to formulas

### Step 2: Create Calculation Script

Create a file named `calculate.sh`:

```bash
#!/bin/bash

# Read input file
source $1

# Simulate calculation time
sleep 1

# Calculate pressure using ideal gas law
# P = nRT/V (R = 8.314 J/(mol·K))
echo 'pressure = '`echo "scale=4;$n_mol*8.314*$T_kelvin/$V_m3" | bc` > output.txt

echo 'Done'
```

Make it executable:

```bash
chmod +x calculate.sh
```

### Step 3: Run Parametric Study

Create a file named `run_study.py`:

```python
import fz

# Define the model
model = {
    "varprefix": "$",           # Variables are marked with $
    "formulaprefix": "@",       # Formulas are marked with @
    "delim": "()",              # Formula delimiters
    "commentline": "#",         # Comment character
    "output": {
        "pressure": "grep 'pressure = ' output.txt | awk '{print $3}'"
    }
}

# Define parameter values
input_variables = {
    "T_celsius": [10, 20, 30, 40],  # 4 temperatures
    "V_L": [1, 2, 5],                # 3 volumes
    "n_mol": 1.0                     # fixed amount
}

# Run all combinations (4 × 3 = 12 cases)
results = fz.fzr(
    "input.txt",
    input_variables,
    model,
    calculators="sh://bash calculate.sh",
    results_dir="results"
)

# Display results
print(results)
print(f"\nCompleted {len(results)} calculations")
```

### Step 4: Execute

Run the study:

```bash
python run_study.py
```

**Expected output:**

```
   T_celsius  V_L  n_mol     pressure status calculator       error command
0         10  1.0    1.0  2353.58     done     sh://        None    bash...
1         10  2.0    1.0  1176.79     done     sh://        None    bash...
2         10  5.0    1.0   470.72     done     sh://        None    bash...
3         20  1.0    1.0  2437.30     done     sh://        None    bash...
...

Completed 12 calculations
```

## Understanding the Results

The results DataFrame contains:

- **Input variables**: `T_celsius`, `V_L`, `n_mol`
- **Output variables**: `pressure`
- **Metadata**: `status`, `calculator`, `error`, `command`

You can use pandas to analyze:

```python
# Find maximum pressure
max_pressure = results['pressure'].max()
print(f"Maximum pressure: {max_pressure}")

# Filter results
high_temp = results[results['T_celsius'] > 25]
print(high_temp)

# Plot results
import matplotlib.pyplot as plt

for volume in results['V_L'].unique():
    data = results[results['V_L'] == volume]
    plt.plot(data['T_celsius'], data['pressure'], 
             marker='o', label=f'V={volume} L')

plt.xlabel('Temperature (°C)')
plt.ylabel('Pressure (Pa)')
plt.legend()
plt.show()
```

## What Just Happened?

Let's break down the workflow:

1. **fzi (Parse Input)** - FZ identified variables `$n_mol`, `$T_celsius`, `$V_L` in `input.txt`

2. **fzc (Compile)** - For each parameter combination, FZ:
   - Created a directory (e.g., `results/T_celsius=10,V_L=1`)
   - Substituted variable values
   - Evaluated formulas
   - Saved compiled input file

3. **Calculator Execution** - For each case, FZ:
   - Ran `bash calculate.sh input.txt` in the case directory
   - Captured output and errors
   - Logged execution metadata

4. **fzo (Parse Output)** - FZ:
   - Ran the output command to extract `pressure`
   - Collected results from all cases
   - Built a pandas DataFrame

5. **fzr (Complete Run)** - FZ orchestrated all steps automatically!

## Next Steps

### Try Different Calculators

Run on a remote server:

```python
results = fz.fzr(
    "input.txt",
    input_variables,
    model,
    calculators="ssh://user@server.com/bash /path/to/calculate.sh",
    results_dir="remote_results"
)
```

Use caching to avoid recalculation:

```python
results = fz.fzr(
    "input.txt",
    input_variables,
    model,
    calculators=[
        "cache://results",           # Check cache first
        "sh://bash calculate.sh"     # Run if not cached
    ],
    results_dir="cached_results"
)
```

### Run in Parallel

Use multiple calculators for parallel execution:

```python
results = fz.fzr(
    "input.txt",
    input_variables,
    model,
    calculators=[
        "sh://bash calculate.sh",
        "sh://bash calculate.sh",
        "sh://bash calculate.sh",
        "sh://bash calculate.sh"
    ],  # 4 parallel workers
    results_dir="parallel_results"
)
```

### Save Model as Alias

Create `.fz/models/perfectgas.json`:

```json
{
    "varprefix": "$",
    "formulaprefix": "@",
    "delim": "()",
    "commentline": "#",
    "output": {
        "pressure": "grep 'pressure = ' output.txt | awk '{print $3}'"
    },
    "id": "perfectgas"
}
```

Then use by name:

```python
results = fz.fzr(
    "input.txt",
    input_variables,
    "perfectgas",  # Model name instead of dict
    calculators="sh://bash calculate.sh",
    results_dir="results"
)
```

## Common Patterns

### Single Parameter Study

Vary one parameter:

```python
results = fz.fzr(
    "input.txt",
    {"temperature": [100, 200, 300, 400, 500]},
    model,
    calculators="sh://bash calc.sh"
)
```

### Full Factorial Design

Vary multiple parameters:

```python
results = fz.fzr(
    "input.txt",
    {
        "param1": [1, 2, 3],      # 3 values
        "param2": [10, 20],       # 2 values
        "param3": [0.1, 0.5, 1.0] # 3 values
    },  # Total: 3 × 2 × 3 = 18 cases
    model,
    calculators="sh://bash calc.sh"
)
```

### Mixed Fixed and Variable Parameters

```python
results = fz.fzr(
    "input.txt",
    {
        "variable_param": [1, 2, 3, 4],  # Variable
        "fixed_param": 100                # Fixed
    },
    model,
    calculators="sh://bash calc.sh"
)
```

## Troubleshooting

**Issue**: Calculation fails with "command not found"

```python
# Use absolute paths
calculators="sh://bash /full/path/to/calculate.sh"
```

**Issue**: Output not parsed correctly

```python
# Test your output command manually
import subprocess
result = subprocess.run(
    "grep 'pressure = ' output.txt | awk '{print $3}'",
    shell=True, capture_output=True, text=True
)
print(result.stdout)
```

**Issue**: Formulas not evaluating

```python
# Check formula syntax
# Ensure variables are marked with $ and formulas with @
# Check that commentline is correct
```

## Google Colab Quick Start

Want to try FZ without installing anything locally? Use Google Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Funz/fz/blob/main/notebooks/quickstart.ipynb)

## Further Reading

- [Core Concepts](concepts.md) - Understand FZ fundamentals
- [Core Functions](../user-guide/core-functions/fzi.md) - Deep dive into fzi, fzc, fzo, fzr
- [Model Definition](../user-guide/model-definition.md) - Learn about model configuration
- [Examples](../examples/perfectgas.md) - More complete examples
