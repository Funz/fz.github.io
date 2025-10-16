# FZ - Parametric Scientific Computing Framework

[![CI](https://github.com/Funz/fz/workflows/CI/badge.svg)](https://github.com/Funz/fz/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Version](https://img.shields.io/badge/version-0.9.0-blue.svg)](https://github.com/Funz/fz/releases)

A powerful Python package for parametric simulations and computational experiments. **FZ** wraps your simulation codes to automatically run parametric studies, manage input/output files, handle parallel execution, and collect results in structured DataFrames.

## What is FZ?

FZ is a framework that simplifies running parametric computational studies. Whether you're working with scientific simulations, engineering calculations, or any computational model, FZ helps you:

- 🔄 **Run parametric studies** - Automatically generate and execute all combinations of parameter values
- ⚡ **Parallelize execution** - Run multiple cases concurrently across multiple calculators
- 💾 **Cache results** - Reuse previous calculations based on input file hashes
- 🌐 **Execute remotely** - Run calculations on remote servers via SSH
- 📊 **Structure output** - Get results as pandas DataFrames with automatic type conversion

## Four Core Functions

FZ provides four fundamental functions that cover the entire workflow:

| Function | Purpose | Description |
|----------|---------|-------------|
| **[fzi](user-guide/core-functions/fzi.md)** | Parse **I**nput | Identify variables in input files |
| **[fzc](user-guide/core-functions/fzc.md)** | **C**ompile | Substitute variable values in templates |
| **[fzo](user-guide/core-functions/fzo.md)** | Parse **O**utput | Extract results from output files |
| **[fzr](user-guide/core-functions/fzr.md)** | **R**un | Execute complete parametric studies |

## Quick Example

Here's a simple parametric study in just a few lines:

```python
import fz

# Define the model
model = {
    "varprefix": "$",
    "output": {
        "pressure": "grep 'pressure = ' output.txt | awk '{print $3}'"
    }
}

# Run all combinations (4 × 3 = 12 cases)
results = fz.fzr(
    "input.txt",
    {
        "T_celsius": [10, 20, 30, 40],  # 4 temperatures
        "V_L": [1, 2, 5],                # 3 volumes
        "n_mol": 1.0                     # fixed amount
    },
    model,
    calculators="sh://bash calculate.sh",
    results_dir="results"
)

print(results)  # pandas DataFrame with all results
```

## Key Features

### Parametric Studies
Generate and run all combinations of parameter values automatically. FZ creates the Cartesian product of your parameter lists and manages execution.

### Multiple Calculators
Execute calculations using different methods:

- **Local shell** - Run scripts and executables locally
- **SSH remote** - Execute on remote servers with automatic file transfer
- **Cache** - Reuse previous results based on input hashes

### Smart Parallel Execution
FZ automatically parallelizes your calculations across available calculators with:

- Load balancing
- Automatic retry on failures
- Progress tracking with ETA
- Graceful interrupt handling (Ctrl+C)

### Formula Evaluation
Use Python or R expressions directly in input templates for calculated parameters:

```text
Temperature: $T_celsius C
# Calculated value
T_kelvin: @($T_celsius + 273.15) K
```

## Getting Started

Ready to get started? Check out our guides:

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } __Quick Start__

    ---

    Get up and running with FZ in minutes

    [:octicons-arrow-right-24: Quick Start](getting-started/quickstart.md)

-   :material-book-open-variant:{ .lg .middle } __User Guide__

    ---

    Learn about core functions, models, and calculators

    [:octicons-arrow-right-24: User Guide](user-guide/core-functions/fzi.md)

-   :material-puzzle:{ .lg .middle } __Plugins__

    ---

    Explore FZ plugins for specific simulation codes

    [:octicons-arrow-right-24: Plugins](plugins/index.md)

-   :material-code-braces:{ .lg .middle } __Examples__

    ---

    See FZ in action with complete examples and Google Colab notebooks

    [:octicons-arrow-right-24: Examples](examples/perfectgas.md)

</div>

## Plugins

FZ includes plugins for various simulation codes:

- **[FZ-Moret](plugins/moret.md)** - Moret model plugin
- **[FZ-MCNP](plugins/mcnp.md)** - Monte Carlo N-Particle Transport Code
- **[FZ-Cathare](plugins/cathare.md)** - Thermal-hydraulic system code
- **[FZ-Cristal](plugins/cristal.md)** - Cristal simulation plugin
- **[FZ-Scale](plugins/scale.md)** - Scale nuclear analysis code
- **[FZ-Telemac](plugins/telemac.md)** - Hydrodynamics simulation system

## Google Colab Integration

Try FZ directly in your browser with our Google Colab notebooks:

- [Basic Example - Perfect Gas](examples/colab.md#perfect-gas-example)
- [OpenModelica Integration](examples/colab.md#openmodelica-example)
- [Plugin Examples](examples/colab.md#plugin-examples)

## Use Cases

FZ is perfect for:

- **Sensitivity Analysis** - Understand how parameters affect your results
- **Design of Experiments** - Systematically explore the parameter space
- **Optimization Studies** - Find optimal parameter combinations
- **Uncertainty Quantification** - Propagate uncertainties through your model
- **Model Validation** - Compare model outputs against experimental data

## Community and Support

- **GitHub**: [Funz/fz](https://github.com/Funz/fz)
- **Issues**: [Report bugs or request features](https://github.com/Funz/fz/issues)
- **Documentation**: You're reading it!

## License

FZ is released under the [BSD 3-Clause License](https://opensource.org/licenses/BSD-3-Clause).

## Citation

If you use FZ in your research, please cite:

```bibtex
@software{fz,
  title = {FZ: Parametric Scientific Computing Framework},
  designers = {[Yann Richet]},
  authors = {[Claude Sonnet, Yann Richet]},
  year = {2025},
  url = {https://github.com/Funz/fz}
}
```
