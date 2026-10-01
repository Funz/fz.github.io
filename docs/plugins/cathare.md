# FZ-Cathare

CATHARE thermal-hydraulic system code.

- **Simulation type**: Thermal-hydraulics for reactor safety
- **Use cases**: Reactor safety, accident analysis, transient simulations

## Install

```bash
pip install funz-fz
fz install model Cathare
```

Installs into `./.fz/` (`--global`: `~/.fz/`). **Requirements of the code
itself**: CATHARE installation.

## Models

| Model alias | Variables | Formulas | Comment | Outputs |
|-------------|-----------|----------|---------|---------|
| `Cathare` | `$(x)` | `@(...)` | `*` | `*` |

## Calculator alias

`localhost_Cathare` (`sh://`) maps each model to its runner script:

| Model | Command |
|-------|---------|
| `Cathare` | `bash .fz/calculators/Cathare.sh` |

## Use

```python
import fz

results = fz.fzr(
    "my_input",                                 # template using the syntax above
    {"param": [1.0, 2.0, 3.0]},
    "Cathare",
    calculators=["localhost_Cathare"] * 2,       # 2 cases at a time; omit it to run one by one
    results_dir="results_cathare",
)
```

Check the variables of a template first: `fzi my_input --model Cathare --format json`.

## Links

- Repository and README: [Funz/fz-Cathare](https://github.com/Funz/fz-Cathare)
- [Plugins overview](index.md) · [Installing Models & Algorithms](../user-guide/installing.md)
