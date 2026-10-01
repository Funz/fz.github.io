# FZ-MCNP

Monte Carlo N-Particle Transport Code support.

- **Simulation type**: Radiation transport, criticality calculations
- **Use cases**: Shielding, criticality, dose calculations

## Install

```bash
pip install funz-fz
fz install model MCNP
```

Installs into `./.fz/` (`--global`: `~/.fz/`). **Requirements of the code
itself**: Set `MCNP_PATH` environment variable.

## Models

| Model alias | Variables | Formulas | Comment | Outputs |
|-------------|-----------|----------|---------|---------|
| `MCNP` | `%(x)` | `@(...)` | `C ` | `mean_keff`, `sigma_keff` |

## Calculator alias

`localhost_MCNP` (`sh://`) maps each model to its runner script:

| Model | Command |
|-------|---------|
| `MCNP` | `bash .fz/calculators/MCNP.sh` |

## Use

```python
import fz

results = fz.fzr(
    "my_input",                                 # template using the syntax above
    {"param": [1.0, 2.0, 3.0]},
    "MCNP",
    calculators=["localhost_MCNP"] * 2,       # 2 cases at a time; omit it to run one by one
    results_dir="results_mcnp",
)
```

Check the variables of a template first: `fzi my_input --model MCNP --format json`.

## Links

- Repository and README: [Funz/fz-MCNP](https://github.com/Funz/fz-MCNP)
- [Plugins overview](index.md) · [Installing Models & Algorithms](../user-guide/installing.md)
