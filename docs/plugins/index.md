# FZ Plugins

FZ plugins extend the framework with specialized support for specific simulation codes and computational models.

## Available Plugins

### Nuclear & Radiation Transport

#### [FZ-MCNP](mcnp.md)
Monte Carlo N-Particle Transport Code support.

- **Simulation type**: Radiation transport
- **Repository**: [Funz/fz-mcnp](https://github.com/Funz/fz-mcnp)
- **Use cases**: Shielding, criticality, dose calculations

#### [FZ-Scale](scale.md)
SCALE nuclear analysis code system.

- **Simulation type**: Nuclear criticality, shielding, isotopic analysis
- **Repository**: [Funz/fz-scale](https://github.com/Funz/fz-scale)
- **Use cases**: Reactor physics, fuel cycle, depletion

### Thermal-Hydraulics

#### [FZ-Cathare](cathare.md)
CATHARE thermal-hydraulic system code.

- **Simulation type**: Thermal-hydraulics
- **Repository**: [Funz/fz-cathare](https://github.com/Funz/fz-cathare)
- **Use cases**: Reactor safety, accident analysis

### Hydrodynamics

#### [FZ-Telemac](telemac.md)
TELEMAC-MASCARET hydrodynamics suite.

- **Simulation type**: Free surface flow, sediment transport
- **Repository**: [Funz/fz-telemac](https://github.com/Funz/fz-telemac)
- **Use cases**: River flow, coastal modeling, dam breaks

### Specialized Models

#### [FZ-Moret](moret.md)
Moret model plugin.

- **Simulation type**: Specialized computational model
- **Repository**: [Funz/fz-moret](https://github.com/Funz/fz-moret)
- **Use cases**: Domain-specific simulations

#### [FZ-Cristal](cristal.md)
Cristal simulation support.

- **Simulation type**: Specialized simulations
- **Repository**: [Funz/fz-cristal](https://github.com/Funz/fz-cristal)
- **Use cases**: Custom computational models

## Plugin Architecture

FZ plugins provide:

1. **Pre-configured models** - Ready-to-use model definitions
2. **Input templates** - Standard input file formats
3. **Output parsers** - Specialized result extraction
4. **Documentation** - Domain-specific guides
5. **Examples** - Working demonstrations

### Plugin Structure

```python
from fz_plugin import get_model, get_calculator

# Get pre-configured model
model = get_model('standard')

# Get calculator for the code
calculator = get_calculator('local')  # or 'cluster', 'docker', etc.

# Run with FZ
import fz
results = fz.fzr(
    "input_template.txt",
    variables,
    model,
    calculators=calculator
)
```

## Installing Plugins

### From Source

```bash
# Clone plugin repository
git clone https://github.com/Funz/fz-<plugin>.git
cd fz-<plugin>

# Install
pip install -e .
```

### In Google Colab

```python
!pip install git+https://github.com/Funz/fz-<plugin>.git
```

## Using Plugins

### Basic Usage

```python
import fz
from fz_mcnp import get_model

# Use plugin model
model = get_model('criticality')

# Define parameters
variables = {
    "enrichment": [2.0, 3.0, 4.0, 5.0],
    "radius": [10, 15, 20],
    "height": [30, 40, 50]
}

# Run parametric study
results = fz.fzr(
    "reactor.inp",
    variables,
    model,
    calculators="sh://mcnp6 i=reactor.inp",
    results_dir="mcnp_results"
)
```

### With Custom Calculator

```python
# Define calculator for HPC
calculator = "ssh://user@cluster.edu/module load mcnp && mcnp6"

results = fz.fzr(
    "reactor.inp",
    variables,
    model,
    calculators=calculator,
    results_dir="mcnp_hpc_results"
)
```

## Plugin Models

Each plugin provides pre-configured models for common use cases.

### Example: FZ-MCNP Models

```python
from fz_mcnp import list_models, get_model

# List available models
models = list_models()
print(models)
# ['criticality', 'shielding', 'dose', 'activation']

# Get specific model
criticality_model = get_model('criticality')
print(criticality_model)
# {
#     'varprefix': '$',
#     'output': {
#         'k_eff': 'grep "final result" output | ...',
#         'k_err': '...'
#     }
# }
```

## Creating Your Own Plugin

### Plugin Template

```python
# fz_myplugin/__init__.py

# Pre-defined models
MODELS = {
    'standard': {
        'varprefix': '$',
        'formulaprefix': '@',
        'output': {
            'result1': 'grep ...',
            'result2': 'grep ...'
        }
    }
}

def get_model(name='standard'):
    """Get pre-configured model"""
    if name not in MODELS:
        raise ValueError(f"Model {name} not found")
    return MODELS[name]

def get_calculator(env='local'):
    """Get calculator URI for environment"""
    calculators = {
        'local': 'sh://mysim',
        'cluster': 'ssh://user@cluster/mysim',
        'docker': 'sh://docker run mysim'
    }
    return calculators.get(env, calculators['local'])
```

### Plugin setup.py

```python
from setuptools import setup, find_packages

setup(
    name='fz-myplugin',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['fz>=0.9.0'],
    author='Your Name',
    description='FZ plugin for MySimulation',
    url='https://github.com/yourusername/fz-myplugin',
)
```

## Plugin Examples

### FZ-MCNP Example

```python
import fz
from fz_mcnp import get_model

model = get_model('shielding')

results = fz.fzr(
    "shield.inp",
    {
        "thickness": [5, 10, 15, 20],  # cm
        "material": ["concrete", "lead", "steel"]
    },
    model,
    calculators="sh://mcnp6 i=shield.inp",
    results_dir="shielding_study"
)

# Analyze dose reduction
print(results.groupby('material')['dose_rate'].mean())
```

### FZ-Telemac Example

```python
import fz
from fz_telemac import get_model

model = get_model('2d_flow')

results = fz.fzr(
    "river.cas",
    {
        "discharge": [100, 200, 500, 1000],  # m³/s
        "roughness": [0.02, 0.03, 0.04]      # Manning's n
    },
    model,
    calculators="sh://telemac2d river.cas",
    results_dir="flood_analysis"
)

# Extract peak water level
print(results.groupby('discharge')['max_water_level'].describe())
```

## Plugin Best Practices

### 1. Provide Multiple Models

```python
MODELS = {
    'simple': {...},      # Basic use case
    'advanced': {...},    # Advanced features
    'validation': {...}   # Model validation
}
```

### 2. Include Input Templates

```
fz_myplugin/
├── __init__.py
├── models.py
├── templates/
│   ├── basic_input.txt
│   ├── advanced_input.txt
│   └── validation_input.txt
└── examples/
    └── example_study.py
```

### 3. Document Output Variables

```python
MODELS = {
    'standard': {
        'output': {
            'k_eff': 'grep "k-eff" ...',     # Effective multiplication factor
            'k_err': 'grep "error" ...',     # Statistical uncertainty
            'runtime': 'grep "time" ...'     # Computation time (s)
        }
    }
}
```

### 4. Provide Validation

```python
def validate_input(variables):
    """Validate input parameters"""
    if variables.get('temperature', 0) < 0:
        raise ValueError("Temperature must be positive")
    # More validation...
```

## Plugin Documentation

Each plugin should include:

- **README.md** - Overview and quick start
- **Installation guide** - Setup instructions
- **Model reference** - Available models and outputs
- **Examples** - Working demonstrations
- **API reference** - Function documentation

## Community Plugins

Want to contribute a plugin?

1. Fork the [FZ plugin template](https://github.com/Funz/fz-plugin-template)
2. Implement your plugin
3. Add tests and documentation
4. Submit a pull request

## Next Steps

Explore specific plugins:

- [FZ-Moret](moret.md) - Moret model
- [FZ-MCNP](mcnp.md) - Monte Carlo N-Particle
- [FZ-Cathare](cathare.md) - Thermal-hydraulics
- [FZ-Cristal](cristal.md) - Cristal simulations
- [FZ-Scale](scale.md) - Nuclear analysis
- [FZ-Telemac](telemac.md) - Hydrodynamics

Or learn more:

- [User Guide](../user-guide/core-functions/fzi.md) - FZ fundamentals
- [Examples](../examples/perfectgas.md) - Complete examples
- [Contributing](../contributing/development.md) - Develop plugins
