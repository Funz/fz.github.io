# Installing Models & Algorithms

Ready-made **models** (wrappers of simulation codes) and **fzd algorithms** are
published as GitHub repositories named `fz-<name>` under the
[Funz organization](https://github.com/orgs/Funz/repositories?q=fz-). fz installs them
into a `.fz/` directory.

## Commands

```bash
fz install model Moret                   # -> https://github.com/Funz/fz-Moret
fz install model https://github.com/you/fz-mycode
fz install model ./fz-mycode.zip         # local archive
fz install model Moret --global          # into ~/.fz/ instead of ./.fz/

fz install algorithm brent               # -> https://github.com/Funz/fz-brent
fz uninstall model Moret
fz uninstall algorithm brent --global
```

```python
fz.install_model("Moret")                        # also fz.install("Moret")
fz.install_algorithm("brent", global_install=True)
fz.list_installed_models()
fz.list_installed_algorithms()
fz.uninstall_model("Moret")
```

| Source | Resolved to |
|--------|-------------|
| Name `X` | `https://github.com/Funz/fz-X`, branch `main` archive |
| GitHub URL | That repository's `main` archive |
| Local `.zip` | The archive itself |

Installing from a network source prints a reminder: the model's templates, formulas and
output commands will run as code with your privileges ([Security](../reference/security.md)).

## What gets installed

A repository ships a `.fz/` tree; every file is copied into `./.fz/` (or `~/.fz/`):

```text
.fz/
├── models/Moret.json                 # model (id, syntax, output extractors); a repo may ship several
├── calculators/Moret.sh              # runner script
├── calculators/localhost_Moret.json  # local alias: {"uri": "sh://", "models": {"Moret": "bash .fz/calculators/Moret.sh"}}
└── algorithms/*.py|*.R               # for algorithm repositories
```

The model is then used by its alias, and the local calculator alias is found
automatically from the model `id`:

```bash
fzr input.inp --model Moret --input_variables '{"e": [1, 2]}' --format json
```

The simulation code itself (MORET, MCNP, ...) is **not** installed: each wrapper's
README states what it expects (path, environment variables).

!!! note "Runner paths"
    Installed aliases run `bash .fz/calculators/<X>.sh`. Such `.fz/...` paths are
    resolved against the `.fz/` directory the alias was loaded from, so a `--global`
    install works from any directory. In fz ≤ 1.2 they were resolved against the launch
    directory, and global installs failed elsewhere (`Command not found locally`).

## Available packages

- Models: see [Plugins](../plugins/index.md) (Moret, MCNP, Cathare, Cristal, Scale,
  Telemac, Modelica, Serpent, Casmo, Cast3M, ...).
- Algorithms: `fz-brent`, `fz-PSO`, `fz-gradientdescent`; the fz repository also ships
  examples in [`examples/algorithms/`](https://github.com/Funz/fz/tree/main/examples/algorithms)
  (random sampling, Monte Carlo, BFGS, Brent, NSGA-II) to copy into `.fz/algorithms/`.

## Checking an installation

```bash
fz list --models Moret --check --format json
```

The model and its `localhost_Moret` calculator alias must both report
`check_status: passed` (fz ≤ 1.2 listed the alias as `sh://` and reported it failed with
`Empty sh:// command`; a real `fzr` run without `--calculators` was then the only check).

## Publishing your own

Template repositories: [fz-Model](https://github.com/Funz/fz-Model),
[fz-Algorithm](https://github.com/Funz/fz-Algorithm),
[fz-AlgorithmR](https://github.com/Funz/fz-AlgorithmR). Use the default branch `main`
(the installer downloads `archive/refs/heads/main.zip`). See also
[Writing Algorithms](design/algorithms.md) and the
[wrapper guide](https://github.com/Funz/fz/blob/main/skills/fz/code-wrapper.md).
