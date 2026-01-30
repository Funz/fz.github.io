# FZ Plugins

FZ plugins extend the framework with specialized support for specific simulation codes and computational models.

## Available Model Plugins

### Nuclear & Radiation Transport

#### [FZ-MCNP](mcnp.md)
Monte Carlo N-Particle Transport Code support.

- **Simulation type**: Radiation transport, criticality calculations
- **Repository**: [Funz/fz-MCNP](https://github.com/Funz/fz-MCNP)
- **Installation**: `pip install git+https://github.com/Funz/fz.git` + Set `MCNP_PATH` environment variable
- **Input syntax**: Variables `%(...)`, Formulas `@{...}`, Comments `C `
- **Main outputs**: `mean_keff`, `sigma_keff`
- **Use cases**: Shielding, criticality, dose calculations

#### [FZ-Moret](moret.md)
MORET Monte Carlo criticality safety calculations.

- **Simulation type**: Reactor physics criticality
- **Repository**: [Funz/fz-Moret](https://github.com/Funz/fz-Moret)
- **Installation**: `fz.install('Moret')` + Install MORET at `/opt/MORET/scripts/moret.py`
- **Input syntax**: Variables `${...}`, Formulas `@{...}`, Comments `*`
- **Main outputs**: `mean_keff`, `sigma_keff`, `dkeff_pertu`, `sigma_dkeff_pertu`
- **Use cases**: Criticality safety, parametric reactor studies

#### [FZ-Cristal](cristal.md)
French criticality package (V1 & V2).

- **Simulation type**: Criticality calculations (SN KEFF, SN Normes, Pij-MC, AP2M5)
- **Repository**: [Funz/fz-Cristal](https://github.com/Funz/fz-Cristal)
- **Installation**: `pip install git+https://github.com/Funz/fz.git` + Set `CRISTAL_HOME` and `CRISTAL_VERSION`
- **Input syntax**: Variables `${...}`, Formulas `@{...}`, Comments `*` (or `#` for XML)
- **Main outputs**: `keff`, `kinf`, `M2`, `B2`, `mean_keff`, `sigma_keff` (model dependent)
- **Use cases**: French nuclear code criticality studies

#### [FZ-Scale](scale.md)
SCALE nuclear analysis code system.

- **Simulation type**: Nuclear criticality, shielding, isotopic analysis, sensitivity
- **Repository**: [Funz/fz-Scale](https://github.com/Funz/fz-Scale)
- **Installation**: `pip install git+https://github.com/Funz/fz.git` + SCALE 6.2+ at `/SCALE/scale6.2` or set `SCALE_HOME`
- **Input syntax**: Variables `&{...}`, Formulas `@{...}`, Comments `'`
- **Main outputs**: `mean_keff`, `sigma_keff`, `mean_E_lethargy`, `mean_nubar`, `mean_free_path`, `lambda` (XSDRNPM)
- **Models**: Scale-keno, Scale-shift, Scale-tsunami, Scale-xsdrnpm
- **Use cases**: Reactor physics, fuel cycle, depletion, sensitivity analysis

#### [FZ-Serpent](https://github.com/Funz/fz-Serpent)
Serpent Monte Carlo reactor physics code.

- **Simulation type**: Continuous-energy Monte Carlo reactor physics
- **Repository**: [Funz/fz-Serpent](https://github.com/Funz/fz-Serpent)
- **Installation**: `pip install git+https://github.com/Funz/fz.git` + `pip install serpentTools` + Serpent2 installation
- **Input syntax**: Variables `${...}`, Formulas `@{...}`, Comments `%`
- **Main outputs**: `absKeff`, `anaKeff`, `colKeff`, `impKeff`, `burnup`, `burnDays` (JSON arrays)
- **Use cases**: Detailed reactor physics, fuel depletion, advanced Monte Carlo simulations

#### [FZ-Casmo](https://github.com/Funz/fz-Casmo)
CASMO5 lattice physics code.

- **Simulation type**: Light water reactor lattice physics
- **Repository**: [Funz/fz-Casmo](https://github.com/Funz/fz-Casmo)
- **Installation**: `pip install git+https://github.com/Funz/fz.git` + CASMO5 license & set `CASMO_PATH`
- **Input syntax**: Variables `${...}`, Formulas `@{...}`, Comments `*`
- **Main outputs**: `k_inf`, `m2`, `burnup`, `u235_wt_pct`, `fissile_pu_wt_pct`, `pin_power_peak` (depletion arrays)
- **Use cases**: PWR/BWR assembly analysis, fuel depletion studies

### Thermal-Hydraulics

#### [FZ-Cathare](cathare.md)
CATHARE thermal-hydraulic system code.

- **Simulation type**: Thermal-hydraulics for reactor safety
- **Repository**: [Funz/fz-Cathare](https://github.com/Funz/fz-Cathare)
- **Installation**: `pip install fz` + CATHARE installation
- **Input syntax**: Variables `$(...)`, Formulas `@(...)`, Comments `*`
- **Main outputs**: EVOLUTION data from FORT07 (TIME_*, Z_* variables with time series)
- **Use cases**: Reactor safety, accident analysis, transient simulations

### Hydrodynamics

#### [FZ-Telemac](telemac.md)
TELEMAC-MASCARET hydrodynamics suite.

- **Simulation type**: Free surface flow, sediment transport
- **Repository**: [Funz/fz-Telemac](https://github.com/Funz/fz-Telemac)
- **Installation**: `pip install git+https://github.com/Funz/fz.git` + `pip install PyTelTools` + Telemac (or Docker)
- **Input syntax**: Variables `$(...)`, Formulas `@(...)`, Comments `/`
- **Main outputs**: `S`, `H` (water surface, depth time series at POI from CSV)
- **Use cases**: River flow, coastal modeling, dam breaks, flood analysis

### Structural & Multi-Physics

#### [FZ-Cast3M](https://github.com/Funz/fz-Cast3M)
Cast3m finite element software.

- **Simulation type**: Structural and fluid mechanics FEM
- **Repository**: [Funz/fz-Cast3M](https://github.com/Funz/fz-Cast3M)
- **Installation**: `pip install git+https://github.com/Funz/fz.git` + Cast3m (castem2000/cast3m in PATH)
- **Input syntax**: Variables `$(...)`, Formulas `%(...)`, Comments `*`
- **Main outputs**: MESS variables, text files (*.txt), CSV files (*.csv)
- **Use cases**: Structural mechanics, thermal analysis, coupled simulations

#### [FZ-Modelica](https://github.com/Funz/fz-Modelica)
OpenModelica multi-physics simulation.

- **Simulation type**: Multi-domain modeling (mechanics, thermodynamics, electrical, control)
- **Repository**: [Funz/fz-Modelica](https://github.com/Funz/fz-Modelica)
- **Installation**: `pip install git+https://github.com/Funz/fz.git` + OpenModelica installation
- **Input syntax**: Variables `${...~default}`, Formulas `@{...}`, Comments `//`
- **Main outputs**: `res` (JSON dictionary with all CSV simulation results)
- **Use cases**: Physical system modeling, control systems, thermal analysis

## Optimization & Design Plugins

#### [FZ-Brent](https://github.com/Funz/fz-brent)
Brent's method for 1D optimization.

- **Type**: Optimization algorithm
- **Repository**: [Funz/fz-brent](https://github.com/Funz/fz-brent)
- **Language**: R
- **Use cases**: Single-variable optimization, root finding

#### [FZ-GradientDescent](https://github.com/Funz/fz-gradientdescent)
Gradient descent optimization.

- **Type**: Optimization algorithm
- **Repository**: [Funz/fz-gradientdescent](https://github.com/Funz/fz-gradientdescent)
- **Language**: R
- **Use cases**: Multi-variable optimization, machine learning

#### [FZ-PSO](https://github.com/Funz/fz-PSO)
Particle Swarm Optimization.

- **Type**: Optimization algorithm
- **Repository**: [Funz/fz-PSO](https://github.com/Funz/fz-PSO)
- **Use cases**: Global optimization, non-convex problems

## Creating Your Own Plugin

### [FZ-Model](https://github.com/Funz/fz-Model)
Generic template repository for creating new fz model plugins.

- **Type**: Plugin template
- **Repository**: [Funz/fz-Model](https://github.com/Funz/fz-Model)
- **Purpose**: Starting point for new simulation code integrations
- **Includes**: Example structure, documentation templates, test framework

## Plugin Architecture

FZ plugins typically include:

1. **Model definition** (`.fz/models/*.json`) - Variable syntax, output parsing rules
2. **Calculator scripts** (`.fz/calculators/*.sh`) - Execution wrapper for simulation code
3. **Calculator configuration** (`.fz/calculators/*.json`) - URI and model mappings
4. **Examples** - Working input files and usage demonstrations
5. **Tests** - Validation suite for the plugin

### Basic Plugin Usage

```python
import fz

# Run parametric study using a plugin
results = fz.fzr(
    input_path="simulation_input.ext",
    input_variables={
        "param1": [1.0, 2.0, 3.0],
        "param2": [0.5, 1.0]
    },
    model="ModelName",  # From plugin's .fz/models/
    calculators="localhost_ModelName",  # From plugin's .fz/calculators/
    results_dir="my_results"
)
```

## Installing Plugins

Most plugins are used directly by cloning their repositories:

```bash
# Clone plugin repository
git clone https://github.com/Funz/fz-<PluginName>.git
cd fz-<PluginName>

# The .fz/ directory is automatically detected by fz
# Install simulation code separately (MCNP, OpenModelica, etc.)
```

Some plugins provide Python installation via `fz.install()`:

```python
import fz
fz.install('Moret')  # Installs Moret plugin
```

## Quick Start with a Plugin

1. **Install fz framework**: `pip install git+https://github.com/Funz/fz.git`
2. **Clone plugin**: `git clone https://github.com/Funz/fz-<PluginName>.git`
3. **Install simulation code**: Follow plugin's README for code installation
4. **Run example**: Check plugin's `examples/` directory or README

## Using Plugins

### Example: Running a Parametric Study

```python
import fz

# Run parametric study with FZ-MCNP plugin
results = fz.fzr(
    input_path="examples/godiva.inp",
    input_variables={
        "r": [8.5, 8.741, 9.0]  # Sphere radius
    },
    model="MCNP",
    calculators="localhost_MCNP",
    results_dir="mcnp_results"
)

print(results[['r', 'mean_keff', 'sigma_keff']])
```

### Example: Remote Execution

```python
# Run on remote HPC cluster via SSH
results = fz.fzr(
    input_path="input.inp",
    input_variables={"enrichment": [3.0, 4.0, 5.0]},
    model="MCNP",
    calculators="ssh://user@hpc.edu/bash /path/to/calculators/MCNP.sh",
    results_dir="remote_results"
)
```

### Example: Parallel Execution

```python
# Use multiple local calculator instances for parallelization
results = fz.fzr(
    input_path="simulation.inp",
    input_variables={"param": list(range(100))},
    model="MyModel",
    calculators=["localhost_MyModel"] * 4,  # 4 parallel workers
    results_dir="parallel_results"
)
```

## Next Steps

Explore specific plugins:

- [FZ-Moret](moret.md) - MORET Monte Carlo criticality
- [FZ-MCNP](mcnp.md) - Monte Carlo N-Particle transport
- [FZ-Cathare](cathare.md) - Thermal-hydraulics
- [FZ-Cristal](cristal.md) - French criticality package
- [FZ-Scale](scale.md) - SCALE nuclear analysis
- [FZ-Telemac](telemac.md) - Hydrodynamics

Or learn more:

- [Installation Guide](../getting-started/installation.md) - Get started with FZ
- [User Guide](../user-guide/core-functions/fzi.md) - FZ fundamentals
- [Examples](../examples/perfectgas.md) - Complete examples
- [Contributing](../contributing/development.md) - Develop your own plugins
