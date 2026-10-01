# FZ-Scale

SCALE nuclear analysis code system.

- **Simulation type**: Nuclear criticality, shielding, isotopic analysis, sensitivity
- **Use cases**: Reactor physics, fuel cycle, depletion, sensitivity analysis

## Install

```bash
pip install funz-fz
fz install model Scale
```

Installs into `./.fz/` (`--global`: `~/.fz/`). **Requirements of the code
itself**: SCALE 6.2+ at `/SCALE/scale6.2` or set `SCALE_HOME`.

## Models

| Model alias | Variables | Formulas | Comment | Outputs |
|-------------|-----------|----------|---------|---------|
| `Scale-keno` | `&(x)` | `@{...}` | `'` | `mean_keff`, `sigma_keff`, `mean_E_lethargy`, `sigma_E_lethargy`, `mean_nubar`, `sigma_nubar`, `mean_free_path`, `sigma_free_path` |
| `Scale-shift` | `&(x)` | `@{...}` | `'` | `mean_keff`, `sigma_keff`, `mean_E_lethargy`, `sigma_E_lethargy`, `mean_nubar`, `sigma_nubar`, `mean_free_path`, `sigma_free_path` |
| `Scale-tsunami` | `&(x)` | `@{...}` | `'` | `mean_keff`, `sigma_keff`, `mean_E_lethargy`, `sigma_E_lethargy`, `mean_nubar`, `sigma_nubar`, `mean_free_path`, `sigma_free_path`, `mean_sens_h1_total`, `sigma_sens_h1_total`, `mean_sens_h1_scatter`, `sigma_sens_h1_scatter`, `mean_sens_h1_capture`, `sigma_sens_h1_capture`, `mean_sens_u235_total`, `sigma_sens_u235_total`, `mean_sens_u235_fission`, `sigma_sens_u235_fission`, `mean_sens_u238_total`, `sigma_sens_u238_total` |
| `Scale-xsdrnpm` | `&(x)` | `@{...}` | `'` | `lambda` |

## Calculator alias

`localhost_Scale` (`sh://`) maps each model to its runner script:

| Model | Command |
|-------|---------|
| `Scale-keno` | `bash .fz/calculators/Scale-keno.sh` |
| `Scale-shift` | `bash .fz/calculators/Scale-shift.sh` |
| `Scale-tsunami` | `bash .fz/calculators/Scale-tsunami.sh` |
| `Scale-xsdrnpm` | `bash .fz/calculators/Scale-xsdrnpm.sh` |

## Use

```python
import fz

results = fz.fzr(
    "my_input",                                 # template using the syntax above
    {"param": [1.0, 2.0, 3.0]},
    "Scale-keno",
    calculators=["localhost_Scale"] * 2,       # 2 cases at a time; omit it to run one by one
    results_dir="results_scale",
)
```

Check the variables of a template first: `fzi my_input --model Scale-keno --format json`.

## Links

- Repository and README: [Funz/fz-Scale](https://github.com/Funz/fz-Scale)
- [Plugins overview](index.md) · [Installing Models & Algorithms](../user-guide/installing.md)
