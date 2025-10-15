# Google Colab Notebooks

Run FZ examples directly in your browser with Google Colab - no installation required!

## What is Google Colab?

[Google Colab](https://colab.research.google.com/) is a free cloud-based Jupyter notebook environment. It's perfect for trying FZ without setting up a local environment.

## Available Notebooks

### 1. Perfect Gas Example

Learn FZ basics with the ideal gas law.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Funz/fz.github.io/blob/main/notebooks/perfectgas_example.ipynb)

**What you'll learn:**

- Installing FZ in Colab
- Creating input templates with variables and formulas
- Running parametric studies
- Analyzing results with pandas
- Visualizing with matplotlib

### 2. OpenModelica Integration

Use FZ with OpenModelica for dynamic system simulations.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Funz/fz.github.io/blob/main/notebooks/modelica_example.ipynb)

**What you'll learn:**

- Installing OpenModelica in Colab
- Creating Modelica models
- Parametric simulation with FZ
- Analyzing dynamic system responses

**Example model:**

```modelica
model SimpleOscillator
  parameter Real omega = $omega;  // Natural frequency
  parameter Real zeta = $zeta;    // Damping ratio
  
  Real x(start=1.0);  // Position
  Real v(start=0.0);  // Velocity
  
equation
  der(x) = v;
  der(v) = -omega^2 * x - 2*zeta*omega*v;
end SimpleOscillator;
```

### 3. MCNP Plugin Example

Monte Carlo radiation transport with FZ-MCNP.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Funz/fz.github.io/blob/main/notebooks/mcnp_example.ipynb)

**Prerequisites:**

- MCNP license (demo uses simplified examples)

**What you'll learn:**

- Installing FZ-MCNP plugin
- Setting up MCNP input files
- Running parametric studies for shielding analysis
- Extracting tallies and analyzing results

### 4. Parallel Processing Demo

Understand FZ's parallel execution capabilities.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Funz/fz.github.io/blob/main/notebooks/parallel_demo.ipynb)

**What you'll learn:**

- Configuring multiple calculators
- Load balancing
- Performance comparison: serial vs parallel
- Monitoring execution

### 5. Caching and Resume

Learn to reuse results and resume interrupted studies.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Funz/fz.github.io/blob/main/notebooks/caching_demo.ipynb)

**What you'll learn:**

- How FZ caching works
- Setting up cache calculators
- Resuming interrupted runs
- Extending previous studies

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
