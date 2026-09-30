# FZ Documentation Website

Source of the documentation site of [FZ](https://github.com/Funz/fz) (PyPI `funz-fz`),
published at **https://funz.github.io/fz.github.io**.

## Structure

| Section | Directory | Content |
|---------|-----------|---------|
| Getting Started | `docs/getting-started/` | Installation, quick start, concepts |
| User Guide — Templates & Models | `docs/user-guide/templates/`, `docs/user-guide/models/` | Template syntax, formulas, model fields, output extraction |
| User Guide — Core Functions | `docs/user-guide/core-functions/` | `fzi`, `fzc`, `fzo`, `fzr`, `fzd`, `fzl` |
| User Guide — Calculators | `docs/user-guide/calculators/` | `sh://`, `ssh://`, `slurm://`/`slurm-array://`, `funz://`, `cache://`, aliases |
| User Guide — Running Studies | `docs/user-guide/running/` | Parallelism, timeouts, caching, results/manifest, interrupts |
| User Guide — other | `docs/user-guide/` | Writing algorithms, installing models, AI agents |
| Plugins | `docs/plugins/` | `fz-<code>` wrappers and algorithms |
| Examples | `docs/examples/` | Perfect gas, Modelica, HPC, Colab |
| Reference | `docs/reference/` | CLI, Python API, `.fz` directory, environment variables, constraints, security, troubleshooting, release notes |
| Contributing | `docs/contributing/` | Development and testing of fz |

Notebooks for Colab are in `notebooks/`. Moved pages are redirected (`redirects` plugin
in `mkdocs.yml`).

## Build

```bash
pip install -r requirements.txt      # MkDocs 1.x + Material; MkDocs 2.0 is not supported
mkdocs serve                         # http://127.0.0.1:8000
mkdocs build --strict                # fails on broken links or anchors
python test_site_structure.py        # every navigation page and redirect was built
```

Pushes to `main` are built with `--strict` and deployed to GitHub Pages by
`.github/workflows/deploy.yml`.

## Writing rules

- Content must match the code of fz: check behavior by running it, not only by reading
  other docs. Constraints that surprise users go to `docs/reference/limitations.md`
  (mirrors `doc/limitations.md` in the fz repository).
- Python examples call `fz.fzr(...)` with `calculators=` and `results_dir=` as keywords.
- Models in examples set `"delim"` explicitly.
- One topic per page; link instead of repeating.

## License

BSD 3-Clause, as [FZ](https://github.com/Funz/fz).
