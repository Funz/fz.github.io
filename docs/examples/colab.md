# Google Colab Notebooks

Run FZ examples directly in your browser with Google Colab - no installation required!

## What is Google Colab?

[Google Colab](https://colab.research.google.com/) is a free cloud-based Jupyter notebook environment. It's perfect for trying FZ without setting up a local environment.

## Available Notebooks

### 1. Getting Started

Core FZ workflow: `fzl`, `fzi`, `fzc`, `fzo`, `fzr` — Perfect Gas PV=nRT end-to-end example.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Funz/fz/blob/main/examples/01_getting_started.ipynb)

**What you'll learn:**

- Installing FZ in Colab
- Listing available models with `fzl`
- Parsing variables with `fzi`
- Compiling templates with `fzc`
- Running parametric studies with `fzr`
- Parsing outputs with `fzo`
- Visualizing results with matplotlib

### 2. Variable Syntax & Formulas

All variable syntaxes, `@{}` formula expressions, `#@` context code, and delimiter styles.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Funz/fz/blob/main/examples/02_variable_syntax_and_formulas.ipynb)

**What you'll learn:**

- `$name`, `${name}`, `${name~default}` variable forms
- `@{expr}` inline formula evaluation (Python & R)
- `#@ code` context blocks and `#@: static` constants
- Legacy `?(name)` syntax
- Custom delimiter styles: `()`, `{}`, `[]`, `<>`

### 3. Parametric Studies (fzr)

Grid and DataFrame inputs, progress callbacks, parallel calculators.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Funz/fz/blob/main/examples/03_parametric_studies_fzr.ipynb)

**What you'll learn:**

- Factorial grid inputs (dict of lists)
- Explicit scenario inputs (DataFrame)
- All callback signatures (`on_start`, `on_case_start`, `on_case_complete`, `on_progress`, `on_complete`)
- Running cases across multiple parallel calculators

### 4. Design of Experiments (fzd)

Adaptive sampling, 1D minimization, N-D optimization, and Monte Carlo.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Funz/fz/blob/main/examples/04_design_of_experiments_fzd.ipynb)

**What you'll learn:**

- Random sampling over a parameter space
- 1D minimization with Brent's method
- N-D optimization with BFGS (Rosenbrock function)
- Monte Carlo estimation of π with convergence analysis

### 5. Caching & Advanced Features

Cache reuse, multi-output models, logging, coarse-to-fine DOE.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Funz/fz/blob/main/examples/05_caching_and_advanced.ipynb)

**What you'll learn:**

- Cold vs warm cache speed comparison
- Numpy array inputs
- Multi-output model parsing
- Logging levels and `print_config()`
- `fzl(check=True)` model validation
- `algorithm_options` tuning
- Coarse-to-fine DOE with `cache://` reuse

## Creating Your Own Colab Notebook

### Step 1: Install FZ

Add this cell at the beginning:

```python
!pip install git+https://github.com/Funz/fz.git
```

For plugins:

```python
!pip install git+https://github.com/Funz/fz-moret.git
```

### Step 2: Install Dependencies

```python
# For OpenModelica
!apt-get update
!apt-get install -y omc

# For visualization
!pip install matplotlib seaborn pandas
```

### Step 3: Create Input Files

```python
%%writefile input.txt
# Your input template
temperature = $temp
pressure = $press
```

### Step 4: Create Calculation Script

```python
%%writefile calculate.sh
#!/bin/bash
source $1
# Your calculation
echo "result = $temp" > output.txt

!chmod +x calculate.sh
```

### Step 5: Run FZ

```python
import fz

model = {
    "varprefix": "$",
    "output": {"result": "grep 'result = ' output.txt | awk '{print $3}'"}
}

results = fz.fzr(
    "input.txt",
    {"temp": [100, 200, 300]},
    model,
    calculators="sh://bash calculate.sh",
    results_dir="results"
)

print(results)
```

## OpenModelica Example

Complete notebook for dynamic system simulations:

```python
# Install OpenModelica
!apt-get update -qq
!apt-get install -y omc

# Install FZ
!pip install git+https://github.com/Funz/fz.git

# Create Modelica model
%%writefile Oscillator.mo
model Oscillator
  parameter Real omega = $omega;  // Natural frequency
  parameter Real zeta = $zeta;    // Damping ratio
  
  Real x(start=1.0);
  Real v(start=0.0);
  
equation
  der(x) = v;
  der(v) = -omega^2 * x - 2*zeta*omega*v;
end Oscillator;

# Create simulation script
%%writefile simulate.sh
#!/bin/bash

# Compile Modelica model
omc -s Oscillator.mo

# Run simulation
./Oscillator -override omega=$omega,zeta=$zeta -r=result.mat

# Extract peak overshoot
python3 << EOF
import scipy.io
mat = scipy.io.loadmat('result.mat')
x = mat['data_2'][0]  # Position data
peak = max(abs(x))
print(f"peak_overshoot = {peak}")
EOF

!chmod +x simulate.sh

# Define FZ model
import fz

model = {
    "varprefix": "$",
    "output": {
        "peak_overshoot": "grep 'peak_overshoot = ' stdout | awk '{print $3}'"
    }
}

# Run parametric study
results = fz.fzr(
    "Oscillator.mo",
    {
        "omega": [1, 2, 5, 10],      # 4 frequencies
        "zeta": [0.1, 0.3, 0.7, 1.0] # 4 damping ratios
    },
    model,
    calculators="sh://bash simulate.sh",
    results_dir="oscillator_results"
)

# Visualize
import matplotlib.pyplot as plt
import seaborn as sns

pivot = results.pivot(index='zeta', columns='omega', values='peak_overshoot')
sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlGn_r')
plt.title('Peak Overshoot: Damping vs Frequency')
plt.show()
```

## Plugins in Colab

### Installing Plugins

```python
# Install base FZ
!pip install git+https://github.com/Funz/fz.git

# Install plugins
!pip install git+https://github.com/Funz/fz-moret.git
!pip install git+https://github.com/Funz/fz-mcnp.git
# etc.
```

### Using Plugin Models

```python
from fz_moret import get_model

# Use plugin model
model = get_model('moret')

results = fz.fzr(
    "input.txt",
    variables,
    model,
    calculators="sh://bash run_moret.sh"
)
```

## Accessing Files in Colab

### Upload Files

```python
from google.colab import files

# Upload input files
uploaded = files.upload()
# Select files from your computer
```

### Download Results

```python
# Download results CSV
results.to_csv('results.csv', index=False)
files.download('results.csv')

# Download all results directory
!zip -r results.zip results/
files.download('results.zip')
```

### Mount Google Drive

```python
from google.colab import drive
drive.mount('/content/drive')

# Save to Drive
results.to_csv('/content/drive/MyDrive/fz_results.csv', index=False)

# Load from Drive
import fz
results = fz.fzo('/content/drive/MyDrive/previous_results', model)
```

## Tips for Colab

### 1. Session Timeout

Colab sessions timeout after inactivity. For long runs:

```python
# Keep session alive
from google.colab import output
output.no_vertical_scroll()

# Save checkpoints
for i in range(0, len(all_cases), 10):
    batch = all_cases[i:i+10]
    results = fz.fzr(...)
    results.to_csv(f'checkpoint_{i}.csv')
```

### 2. GPU/TPU Not Needed

FZ doesn't use GPU/TPU. Use default runtime:

```
Runtime → Change runtime type → Hardware accelerator: None
```

### 3. Install System Packages

```python
# Install bc for calculations
!apt-get install -y bc

# Install simulation tools
!apt-get install -y modelica
```

### 4. Debugging

Enable debug logging:

```python
import os
os.environ['FZ_LOG_LEVEL'] = 'DEBUG'
```

View execution logs:

```python
!cat results/case1/log.txt
```

## Sharing Your Notebook

1. **Save to GitHub**:
   - File → Save a copy in GitHub
   - Choose your repository

2. **Get Colab Link**:
   ```
   https://colab.research.google.com/github/username/repo/blob/main/notebook.ipynb
   ```

3. **Add Badge to README**:
   ```markdown
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/username/repo/blob/main/notebook.ipynb)
   ```

## Example Notebooks Repository

All example notebooks are available at:

[https://github.com/Funz/fz-notebooks](https://github.com/Funz/fz-notebooks)

Clone to customize:

```bash
git clone https://github.com/Funz/fz-notebooks.git
```

## Next Steps

- [Perfect Gas Example](perfectgas.md) - Detailed walkthrough
- [Modelica Integration](modelica.md) - Dynamic systems
- [Plugins](../plugins/index.md) - Explore available plugins
- [User Guide](../user-guide/core-functions/fzi.md) - Deep dive into FZ
