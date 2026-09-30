# FZ-Moret

MORET Monte Carlo criticality safety calculations.

- **Simulation type**: Reactor physics criticality
- **Use cases**: Criticality safety, parametric reactor studies

## Install

```bash
pip install funz-fz
fz install model Moret
```

Installs into `./.fz/` (`--global`: `~/.fz/`, see the
[warning on runner paths](../user-guide/installing.md)). **Requirements of the code
itself**: MORET at `/opt/MORET/scripts/moret.py`.

## Models

| Model alias | Variables | Formulas | Comment | Outputs |
|-------------|-----------|----------|---------|---------|
| `Moret` | `${x}` | `@{...}` | `*` | `mean_keff`, `sigma_keff`, `dkeff_pertu`, `sigma_dkeff_pertu` |

## Calculator alias

`localhost_Moret` (`sh://`) maps each model to its runner script:

| Model | Command |
|-------|---------|
| `Moret` | `bash .fz/calculators/Moret.sh` |

## Use

```python
import fz

results = fz.fzr(
    "my_input",                                 # template using the syntax above
    {"param": [1.0, 2.0, 3.0]},
    "Moret",
    calculators=["localhost_Moret"] * 2,       # 2 cases at a time; omit it to run one by one
    results_dir="results_moret",
)
```

Check the variables of a template first: `fzi my_input --model Moret --format json`.

## Links

- Repository and README: [Funz/fz-Moret](https://github.com/Funz/fz-Moret)
- [Plugins overview](index.md) · [Installing Models & Algorithms](../user-guide/installing.md)
