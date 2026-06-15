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

## Algorithm Plugins

Algorithm plugins are used with [`fzd`](../user-guide/core-functions/fzd.md) for adaptive,
iterative design of experiments. Install them from their GitHub repositories:

```bash
fz install algorithm brent           # → https://github.com/Funz/fz-brent
fz install algorithm gradientdescent # → https://github.com/Funz/fz-gradientdescent
fz install algorithm PSO             # → https://github.com/Funz/fz-PSO
```

!!! note "R requirement"
    These algorithm plugins are implemented in **R**. You need R installed on your system
    plus the `rpy2` Python bridge: `pip install rpy2`.

#### [FZ-Brent](https://github.com/Funz/fz-brent)
Brent's method for 1D root finding / inversion.

- **Repository**: [Funz/fz-brent](https://github.com/Funz/fz-brent)
- **Dimensions**: 1D only
- **Use cases**: Find the input value that produces a target output (inversion/calibration)
- **Key options**:

| Option | Default | Description |
|--------|---------|-------------|
| `ytarget` | `0.0` | Target output value |
| `ytol` | `0.1` | Convergence precision on output |
| `xtol` | `0.01` | Convergence precision on input |
| `max_iterations` | `100` | Maximum iterations |

```python
result = fz.fzd("input.txt", {"x": "[0;1]"}, model,
    output_expression="y", algorithm="brent",
    algorithm_options={"ytarget": 0.5, "ytol": 0.01})
```

#### [FZ-GradientDescent](https://github.com/Funz/fz-gradientdescent)
First-order local optimization via gradient descent (minimization or maximization).

- **Repository**: [Funz/fz-gradientdescent](https://github.com/Funz/fz-gradientdescent)
- **Dimensions**: Multi-dimensional
- **Use cases**: Local optimization of smooth functions; gradient estimated by finite differences
- **Key options**:

| Option | Default | Description |
|--------|---------|-------------|
| `yminimization` | `true` | `false` to maximize |
| `max_iterations` | `100` | Maximum iterations |
| `ytol` | `0.1` | Convergence tolerance on output |
| `delta` | `1` | Initial gradient step factor (auto-adjusted) |
| `epsilon` | `0.01` | Finite-difference step for gradient estimation |
| `x0` | `""` | Starting point (comma-separated), e.g. `"0.5,0.5"` |

```python
result = fz.fzd("input.txt", {"x1": "[0;1]", "x2": "[0;1]"}, model,
    output_expression="y", algorithm="gradientdescent",
    algorithm_options={"yminimization": True, "max_iterations": 50})
```

#### [FZ-PSO](https://github.com/Funz/fz-PSO)
Particle Swarm Optimization — global stochastic optimizer.

- **Repository**: [Funz/fz-PSO](https://github.com/Funz/fz-PSO)
- **Dimensions**: Multi-dimensional
- **Use cases**: Global optimization, non-convex or noisy objectives
- **Key options**:

| Option | Default | Description |
|--------|---------|-------------|
| `yminimization` | `true` | `false` to maximize |
| `max_iterations` | `30` | Maximum iterations |
| `nparticles` | auto | Swarm size (default: `10 + 2√d`) |
| `seed` | `123` | Random seed |
| `w` | `0.7213` | Inertia weight |
| `c_p` | `1.1931` | Cognitive (personal best) coefficient |
| `c_g` | `1.1931` | Social (global best) coefficient |

```python
result = fz.fzd("input.txt", {"x1": "[0;1]", "x2": "[0;1]"}, model,
    output_expression="y", algorithm="PSO",
    algorithm_options={"yminimization": True, "max_iterations": 30, "nparticles": 20})
```

## Creating Your Own Plugin

### [FZ-Model](https://github.com/Funz/fz-Model)
Generic template repository for creating new fz model plugins.

- **Type**: Model plugin template
- **Repository**: [Funz/fz-Model](https://github.com/Funz/fz-Model)
- **Purpose**: Starting point for new simulation code integrations
- **Includes**: Example structure, documentation templates, test framework

### [FZ-Algorithm](https://github.com/Funz/fz-Algorithm) / [FZ-AlgorithmR](https://github.com/Funz/fz-AlgorithmR)
Template repositories for writing custom `fzd` algorithm plugins.

- **Type**: Algorithm plugin template
- **Repositories**: [Funz/fz-Algorithm](https://github.com/Funz/fz-Algorithm) (Python), [Funz/fz-AlgorithmR](https://github.com/Funz/fz-AlgorithmR) (R)
- **Purpose**: Starting point for new optimization, sampling, or calibration algorithms
- **Interface**: implement `get_initial_design`, `get_next_design`, `get_analysis`

See also [Writing Custom Algorithms](../user-guide/core-functions/fzd.md#writing-custom-algorithms) in the fzd docs.

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

**Model plugins**

- [FZ-Moret](moret.md) - MORET Monte Carlo criticality
- [FZ-MCNP](mcnp.md) - Monte Carlo N-Particle transport
- [FZ-Cathare](cathare.md) - Thermal-hydraulics
- [FZ-Cristal](cristal.md) - French criticality package
- [FZ-Scale](scale.md) - SCALE nuclear analysis
- [FZ-Telemac](telemac.md) - Hydrodynamics

**Algorithm plugins**

- [FZ-Brent](https://github.com/Funz/fz-brent) - 1D root finding / inversion
- [FZ-GradientDescent](https://github.com/Funz/fz-gradientdescent) - Local gradient-based optimization
- [FZ-PSO](https://github.com/Funz/fz-PSO) - Global particle swarm optimization

Or learn more:

- [Installation Guide](../getting-started/installation.md) - Get started with FZ
- [User Guide](../user-guide/core-functions/fzi.md) - FZ fundamentals
- [Examples](../examples/perfectgas.md) - Complete examples
- [Contributing](../contributing/development.md) - Develop your own plugins
