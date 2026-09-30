# FZ - Parametric Scientific Computing Framework

[![CI](https://github.com/Funz/fz/workflows/CI/badge.svg)](https://github.com/Funz/fz/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/funz-fz.svg)](https://pypi.org/project/funz-fz/)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

**FZ** wraps any simulation code that reads input files and writes output files, and runs
it as a parametric study: variables in the input files are substituted for each case,
cases run in parallel (locally, over SSH, on SLURM or on Funz servers), and the outputs
are parsed back into a pandas DataFrame. FZ is the Python rewrite of the Java
[Funz](https://github.com/Funz) framework. PyPI package: `funz-fz`.

```bash
pip install funz-fz
```

## Minimal example

```python
import fz

model = {"output": {"pressure": "python://grep(r'pressure = (\\S+)', 'output.txt')"}}

results = fz.fzr(
    "input.txt",                                  # template containing $T_celsius, $V_L
    {"T_celsius": [10, 20, 30], "V_L": [1, 2]},   # 3 x 2 = 6 cases
    model,
    calculators="sh://bash calculate.sh",         # always pass by keyword
    results_dir="results",
)
print(results[["T_celsius", "V_L", "pressure", "status"]])
```

The full walk-through is in the [Quick Start](getting-started/quickstart.md).

## The six functions

Each function exists in Python (`fz.fzr(...)`) and as a command (`fzr ...` or
`fz run ...`).

| Function | Role | Page |
|----------|------|------|
| `fzi` | List the variables of an input template | [fzi](user-guide/core-functions/fzi.md) |
| `fzc` | Compile templates with given values | [fzc](user-guide/core-functions/fzc.md) |
| `fzo` | Parse output files into a table | [fzo](user-guide/core-functions/fzo.md) |
| `fzr` | Run a full parametric study (grid or list of cases) | [fzr](user-guide/core-functions/fzr.md) |
| `fzd` | Run an adaptive design of experiments (optimization, sampling, calibration) | [fzd](user-guide/core-functions/fzd.md) |
| `fzl` | List and check installed models and calculators | [fzl](user-guide/core-functions/fzl.md) |

## How the documentation is organized

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } __Getting Started__

    ---

    Installation, a first study end to end, and the vocabulary (template, model,
    calculator, case).

    [:octicons-arrow-right-24: Quick Start](getting-started/quickstart.md)

-   :material-file-document-edit:{ .lg .middle } __Templates & Models__

    ---

    How to mark variables and formulas in input files, and how to declare the outputs to
    extract.

    [:octicons-arrow-right-24: Template syntax](user-guide/templates/syntax.md)

-   :material-server-network:{ .lg .middle } __Calculators__

    ---

    Where cases run: local shell, SSH, SLURM (per case or job arrays), Funz servers, and
    the result cache.

    [:octicons-arrow-right-24: Calculators](user-guide/calculators/overview.md)

-   :material-play-speed:{ .lg .middle } __Running Studies__

    ---

    Parallelism, retries, timeouts, caching, results layout, manifest, interrupt and
    resume.

    [:octicons-arrow-right-24: Running studies](user-guide/running/parallel.md)

-   :material-chart-bell-curve:{ .lg .middle } __Design of Experiments__

    ---

    `fzd` with built-in or installed algorithms, and how to write your own.

    [:octicons-arrow-right-24: fzd](user-guide/core-functions/fzd.md)

-   :material-alert-circle-outline:{ .lg .middle } __Constraints & Limits__

    ---

    Behaviors that most often surprise users, checked against the code. Read before
    writing a first model.

    [:octicons-arrow-right-24: Constraints](reference/limitations.md)

</div>

## Capabilities at a glance

| Area | What FZ provides | Details |
|------|------------------|---------|
| Templates | `$var`, `${var~default}`, `@{formula}` in Python or R, `#@` context lines, DecimalFormat number formatting, Java Funz `$(var)` templates | [Syntax](user-guide/templates/syntax.md), [Formulas](user-guide/templates/formulas.md) |
| Designs | Full factorial (dict of lists), explicit case list (DataFrame), adaptive (`fzd`) incl. multi-objective | [fzr](user-guide/core-functions/fzr.md), [fzd](user-guide/core-functions/fzd.md) |
| Outputs | Shell commands, shell-free `python://`, `jq://`, `yq://`, `xpath://`, Python callables; scalar or vector values | [Output extraction](user-guide/models/outputs.md) |
| Execution | `sh://`, `ssh://`, `slurm://`, `slurm-array://`, `funz://`, `cache://`; aliases in `.fz/calculators/` | [Calculators](user-guide/calculators/overview.md) |
| Robustness | Retries across calculators, timeouts, graceful Ctrl+C, resume from cache | [Running studies](user-guide/running/parallel.md) |
| Traceability | Per-case logs, `manifest.json`, RO-Crate metadata, cache identity (`code_id`) | [Results & traceability](user-guide/running/results.md) |
| Packaging | `fz install model|algorithm <name>` from the `fz-<name>` repositories | [Installing](user-guide/installing.md), [Plugins](plugins/index.md) |
| AI agents | Claude Code plugin (skill + slash commands), `fz-mcp` MCP server | [AI agents](user-guide/ai-agents.md) |

## Requirements

- Python ≥ 3.9 (tested 3.9–3.13); dependencies `paramiko`, `pandas`, `charset-normalizer`.
- **bash** for shell calculators and shell output commands (MSYS2 or Git Bash on
  Windows, located with `FZ_SHELL_PATH`).
- Optional: `rpy2` + R (R formulas), `mcp` on Python ≥ 3.10 (`fz-mcp`), `h5py`, `jq`,
  `yq`, `xmllint` (corresponding output extractors).

!!! warning "Security"
    Templates, formulas, output commands and calculator commands run as code with your
    privileges. Only use models, algorithms and calculator aliases from sources you
    trust. See [Security Model](reference/security.md).

## Links

- Source and issues: [github.com/Funz/fz](https://github.com/Funz/fz)
- Release notes: [Release Notes](reference/releases.md)
- License: [BSD 3-Clause](https://opensource.org/licenses/BSD-3-Clause)

## Citation

```bibtex
@software{fz,
  title = {FZ: Parametric Scientific Computing Framework},
  designers = {[Yann Richet]},
  authors = {[Claude Sonnet, Yann Richet]},
  year = {2025},
  url = {https://github.com/Funz/fz}
}
```
