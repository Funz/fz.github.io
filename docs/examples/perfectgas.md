# Perfect Gas Pressure Example

This comprehensive example demonstrates a complete parametric study using the ideal gas law. We'll calculate pressure for various combinations of temperature, volume, and amount of gas.

## The Ideal Gas Law

The ideal gas law relates pressure, volume, temperature, and amount of gas:

$$PV = nRT$$

Where:

- **P** = Pressure (Pa)
- **V** = Volume (m³)
- **n** = Amount of substance (mol)
- **R** = Gas constant = 8.314 J/(mol·K)
- **T** = Temperature (K)

## Project Structure

```
perfectgas/
├── input.txt           # Input template
├── calculate.sh        # Calculation script
└── run_study.py        # Python orchestration
```

## Step 1: Input Template

Create `input.txt` with variables and formulas:

```text
# input file for Perfect Gas Pressure, with variables n_mol, T_celsius, V_L
n_mol=$n_mol
T_kelvin=@($T_celsius + 273.15)

#@ def L_to_m3(L):
#@     return(L / 1000)
V_m3=@(L_to_m3($V_L))
```

**Key features:**

- **Variables**: `$n_mol`, `$T_celsius`, `$V_L`
- **Formulas**: Convert Celsius to Kelvin, Liters to m³
- **Functions**: `L_to_m3()` for unit conversion

## Step 2: Calculation Script

Create `calculate.sh`:

```bash
#!/bin/bash

# Read input file
source $1

# Simulate calculation time
sleep 1

# Calculate pressure using ideal gas law
# P = nRT/V where R = 8.314 J/(mol·K)
pressure=$(echo "scale=4; $n_mol * 8.314 * $T_kelvin / $V_m3" | bc)

# Write output
echo "pressure = $pressure" > output.txt
echo "Temperature: $T_celsius °C ($T_kelvin K)" >> output.txt
echo "Volume: $V_L L ($V_m3 m³)" >> output.txt
echo "Amount: $n_mol mol" >> output.txt

echo "Calculation complete"
```

Make executable:

```bash
chmod +x calculate.sh
```

## Step 3: Run Parametric Study

Create `run_study.py`:

```python
import fz
import pandas as pd
import matplotlib.pyplot as plt

# Define the model
model = {
    "varprefix": "$",
    "formulaprefix": "@",
    "delim": "()",
    "commentline": "#",
    "output": {
        "pressure": "grep 'pressure = ' output.txt | awk '{print $3}'"
    }
}

# Define parameter space
input_variables = {
    "n_mol": [1, 2, 3],              # 3 amounts
    "T_celsius": [0, 10, 20, 30, 40], # 5 temperatures
    "V_L": [1, 2, 5, 10]              # 4 volumes
}

# Total cases: 3 × 5 × 4 = 60

# Run parametric study
results = fz.fzr(
    "input.txt",
    input_variables,
    model,
    calculators="sh://bash calculate.sh",
    results_dir="results"
)

# Display summary
print(f"\nCompleted {len(results)} calculations")
print(f"\nResults summary:")
print(results.describe())

# Save results
results.to_csv("perfectgas_results.csv", index=False)
print(f"\nResults saved to perfectgas_results.csv")
```

## Step 4: Execute

Run the study:

```bash
python run_study.py
```

## Results Analysis

### View Results

```python
import pandas as pd

# Load results
results = pd.read_csv("perfectgas_results.csv")

# Show first few rows
print(results.head())

# Filter high pressure cases
high_pressure = results[results['pressure'] > 10000]
print(f"\nHigh pressure cases: {len(high_pressure)}")
```

### Statistical Analysis

```python
# Group by amount of gas
by_amount = results.groupby('n_mol').agg({
    'pressure': ['mean', 'std', 'min', 'max']
})
print("\nPressure statistics by amount:")
print(by_amount)

# Correlation analysis
print("\nCorrelation matrix:")
print(results[['n_mol', 'T_celsius', 'V_L', 'pressure']].corr())
```

## Visualization

### Pressure vs Temperature

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Plot 1: Different volumes
ax = axes[0]
for volume in sorted(results['V_L'].unique()):
    for n in sorted(results['n_mol'].unique()):
        data = results[(results['V_L'] == volume) & (results['n_mol'] == n)]
        ax.plot(data['T_celsius'], data['pressure'],
                marker='o', label=f'n={n} mol, V={volume} L')

ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Pressure (Pa)')
ax.set_title('Ideal Gas: Pressure vs Temperature')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True)

# Plot 2: 3D surface for fixed n=1
ax = axes[1]
from mpl_toolkits.mplot3d import Axes3D
ax = plt.subplot(122, projection='3d')

data_n1 = results[results['n_mol'] == 1]
ax.scatter(data_n1['T_celsius'], data_n1['V_L'], data_n1['pressure'],
           c=data_n1['pressure'], cmap='viridis')
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Volume (L)')
ax.set_zlabel('Pressure (Pa)')
ax.set_title('Pressure Surface (n=1 mol)')

plt.tight_layout()
plt.savefig('perfectgas_analysis.png', dpi=150, bbox_inches='tight')
print("Visualization saved to perfectgas_analysis.png")
```

### Heatmap

```python
import seaborn as sns

# Create pivot table for n=1 mol
pivot_data = results[results['n_mol'] == 1].pivot(
    index='V_L', columns='T_celsius', values='pressure'
)

plt.figure(figsize=(10, 6))
sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='RdYlBu_r')
plt.title('Pressure Heatmap (n=1 mol)')
plt.xlabel('Temperature (°C)')
plt.ylabel('Volume (L)')
plt.savefig('perfectgas_heatmap.png', dpi=150, bbox_inches='tight')
```

## Advanced: Parallel Execution

Run with 4 parallel workers:

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
    ],
    results_dir="results_parallel"
)
```

## Advanced: Remote Execution

Run on an HPC cluster:

```python
results = fz.fzr(
    "input.txt",
    input_variables,
    model,
    calculators="ssh://user@cluster.edu/bash /path/to/calculate.sh",
    results_dir="results_remote"
)
```

## Advanced: Caching

Resume or extend a previous study:

```python
# Extend to more cases
extended_variables = {
    "n_mol": [1, 2, 3, 4, 5],        # Added 4 and 5
    "T_celsius": [0, 10, 20, 30, 40],
    "V_L": [1, 2, 5, 10]
}

# Reuse previous results, only calculate new cases
results = fz.fzr(
    "input.txt",
    extended_variables,
    model,
    calculators=[
        "cache://results",           # Check cache first
        "sh://bash calculate.sh"     # Only run new cases
    ],
    results_dir="results_extended"
)
```

## Google Colab Version

Try this example in Google Colab without any local installation:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Funz/fz.github.io/blob/main/notebooks/perfectgas_example.ipynb)

The notebook includes:

- Automatic FZ installation
- Complete working example
- Interactive visualization
- Downloadable results

## Validation

Verify results against theoretical values:

```python
import numpy as np

def ideal_gas_pressure(n, T_celsius, V_L):
    """Calculate pressure using ideal gas law"""
    R = 8.314  # J/(mol·K)
    T_kelvin = T_celsius + 273.15
    V_m3 = V_L / 1000
    return n * R * T_kelvin / V_m3

# Compare with simulation
for _, row in results.head().iterrows():
    expected = ideal_gas_pressure(row['n_mol'], row['T_celsius'], row['V_L'])
    actual = row['pressure']
    error = abs(expected - actual) / expected * 100
    print(f"n={row['n_mol']}, T={row['T_celsius']}, V={row['V_L']}: "
          f"Expected={expected:.2f}, Actual={actual:.2f}, Error={error:.3f}%")
```

## Complete Working Example

Download all files:

- [input.txt](https://github.com/Funz/fz/blob/main/examples/perfectgas/input.txt)
- [calculate.sh](https://github.com/Funz/fz/blob/main/examples/perfectgas/calculate.sh)
- [run_study.py](https://github.com/Funz/fz/blob/main/examples/perfectgas/run_study.py)

Or clone the examples:

```bash
git clone https://github.com/Funz/fz.git
cd fz/examples/perfectgas
python run_study.py
```

## Next Steps

- [Modelica Example](modelica.md) - OpenModelica integration
- [HPC Example](hpc.md) - Remote cluster execution
- [Advanced Features](../user-guide/advanced/parallel.md) - Master parallel execution
- [Plugins](../plugins/index.md) - Explore FZ plugins
