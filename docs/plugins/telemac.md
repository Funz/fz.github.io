# FZ-Telemac

TELEMAC-MASCARET hydrodynamics suite.

- **Simulation type**: Free surface flow, sediment transport
- **Use cases**: River flow, coastal modeling, dam breaks, flood analysis

## Install

```bash
pip install funz-fz
fz install model Telemac
```

Installs into `./.fz/` (`--global`: `~/.fz/`, see the
[warning on runner paths](../user-guide/installing.md)). **Requirements of the code
itself**: `pip install PyTelTools` + Telemac (or Docker).

## Models

| Model alias | Variables | Formulas | Comment | Outputs |
|-------------|-----------|----------|---------|---------|
| `Telemac` | `$(x)` | `@(...)` | `/` | `S`, `H` |

## Calculator alias

`localhost_Telemac` (`sh://`) maps each model to its runner script:

| Model | Command |
|-------|---------|
| `Telemac` | `bash .fz/calculators/Telemac.sh` |

## Use

```python
import fz

results = fz.fzr(
    "my_input",                                 # template using the syntax above
    {"param": [1.0, 2.0, 3.0]},
    "Telemac",
    calculators=["localhost_Telemac"] * 2,       # 2 cases at a time; omit it to run one by one
    results_dir="results_telemac",
)
```

Check the variables of a template first: `fzi my_input --model Telemac --format json`.

## Links

- Repository and README: [Funz/fz-Telemac](https://github.com/Funz/fz-Telemac)
- [Plugins overview](index.md) · [Installing Models & Algorithms](../user-guide/installing.md)
