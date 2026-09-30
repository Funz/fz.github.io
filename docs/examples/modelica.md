# Modelica / OpenModelica

The [FZ-Modelica](https://github.com/Funz/fz-Modelica) wrapper runs OpenModelica
models as parametric studies.

## Install

```bash
sudo apt-get install omc              # OpenModelica compiler (or the installer for your OS)
pip install funz-fz
fz install model Modelica             # model "Modelica" + localhost_Modelica alias in ./.fz/
```

## Template

Variables use `${...}` (the model sets `delim: "{}"`) and comments are `//`:

```modelica title="NewtonCooling.mo"
model NewtonCooling
  parameter Real T_inf = 25;
  parameter Real T0 = 90;
  parameter Real h = ${convection~0.7};
  parameter Real m = 0.1;
  parameter Real c_p = 1.2;
  parameter Real A = 1.0;
  Real T;
initial equation
  T = T0;
equation
  m*c_p*der(T) = h*A*(T_inf-T);
end NewtonCooling;
```

## Run

```python
import fz

results = fz.fzr(
    "NewtonCooling.mo",
    {"convection": [0.3, 0.7, 1.5]},
    "Modelica",
    calculators=["localhost_Modelica"] * 3,
    results_dir="results_modelica",
)
```

The model's single output `res` is a dict of the simulation's CSV results; `fzr`
expands it into columns `res_<ModelName>_<variable>` (e.g. `res_NewtonCooling_T`), each
holding the time series of one case.

## Notebooks

- [fz_modelica_projectile.ipynb](https://github.com/Funz/fz/blob/main/examples/fz_modelica_projectile.ipynb) in the fz repository
- [Google Colab Notebooks](colab.md)

## Links

[OpenModelica](https://openmodelica.org/) · [Funz/fz-Modelica](https://github.com/Funz/fz-Modelica)
