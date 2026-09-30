# FZ-Cristal

French criticality package (V1 & V2).

- **Simulation type**: Criticality calculations (SN KEFF, SN Normes, Pij-MC, AP2M5)
- **Use cases**: French nuclear code criticality studies

## Install

```bash
pip install funz-fz
fz install model Cristal
```

Installs into `./.fz/` (`--global`: `~/.fz/`, see the
[warning on runner paths](../user-guide/installing.md)). **Requirements of the code
itself**: Set `CRISTAL_HOME` and `CRISTAL_VERSION`.

## Models

| Model alias | Variables | Formulas | Comment | Outputs |
|-------------|-----------|----------|---------|---------|
| `CRISTAL-AP2M5` | `${x}` | `@{...}` | `#` | `mean_keff`, `sigma_keff`, `dkeff_pertu`, `sigma_dkeff_pertu`, `cU`, `cPU`, `M2`, `B2`, `KINF` |
| `Cristal-Pij-MC` | `${x}` | `@{...}` | `*` | `mean_keff`, `sigma_keff`, `dkeff_pertu`, `sigma_dkeff_pertu`, `cU`, `cPU`, `M2`, `B2`, `KINF` |
| `Cristal-SnKeff` | `${x}` | `@{...}` | `*` | `keff`, `kinf`, `slowing_down`, `M2`, `B2` |
| `Cristal-SnNormes` | `${x}` | `@{...}` | `*` | `keff`, `kinf`, `slowing_down`, `M2`, `B2`, `dimension`, `cx`, `hx` |

## Calculator alias

`localhost_Cristal` (`sh://`) maps each model to its runner script:

| Model | Command |
|-------|---------|
| `Cristal-SnKeff` | `bash .fz/calculators/Cristal.sh` |
| `Cristal-SnNormes` | `bash .fz/calculators/Cristal.sh` |
| `Cristal-Pij-MC` | `bash .fz/calculators/Cristal.sh` |
| `CRISTAL-AP2M5` | `bash .fz/calculators/Cristal.sh` |

## Use

```python
import fz

results = fz.fzr(
    "my_input",                                 # template using the syntax above
    {"param": [1.0, 2.0, 3.0]},
    "CRISTAL-AP2M5",
    calculators=["localhost_Cristal"] * 2,       # 2 cases at a time; omit it to run one by one
    results_dir="results_cristal",
)
```

Check the variables of a template first: `fzi my_input --model CRISTAL-AP2M5 --format json`.

## Links

- Repository and README: [Funz/fz-Cristal](https://github.com/Funz/fz-Cristal)
- [Plugins overview](index.md) · [Installing Models & Algorithms](../user-guide/installing.md)
