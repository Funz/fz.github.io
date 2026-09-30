# Development

FZ lives at [github.com/Funz/fz](https://github.com/Funz/fz) (BSD 3-Clause). This page is
a quick orientation for contributors; the canonical instructions are the repo's
`README.md` and `CLAUDE.md`.

## Setup

```bash
git clone https://github.com/Funz/fz.git
cd fz
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"
```

`paramiko` and `pandas` are required dependencies. Optional: `rpy2` + R (R formulas and
algorithms, extra `[r]`), `mcp` (extra `[mcp]`, Python ≥ 3.10), `h5py`, `jq`, `yq`,
`xmllint`.

## Package Layout

| Module | Responsibility |
|--------|----------------|
| `fz/core.py` | Public functions `fzi`, `fzc`, `fzo`, `fzr`, `fzd`, `fzl` |
| `fz/cli.py` | Entry points `fz`, `fzi`, `fzc`, `fzo`, `fzr`, `fzd`, `fzl` |
| `fz/interpreter.py` | Variable parsing, formula evaluation (Python / R) |
| `fz/outparsers.py` | `python://`, `jq://`, `yq://`, `xpath://` output extractors |
| `fz/runners/` | Calculator backends: `sh`, `ssh`, `slurm`, `slurm_array`, `funz`, `cache`, plus `dispatch`, `manager`, `resolve`, `base` |
| `fz/slurm_async.py` | Job-array batching and `sacct` monitoring |
| `fz/helpers.py` | Case scheduling, retries, calculator/model resolution |
| `fz/io.py` | File staging, `.fz_hash`, cache matching |
| `fz/manifest.py`, `fz/uri.py` | `manifest.json` / RO-Crate, URI password redaction |
| `fz/algorithms.py` | `fzd` algorithm loading and output expressions |
| `fz/installer.py` | `fz install` / `fz uninstall` |
| `fz/mcp_server.py` | `fz-mcp` |
| `fz/config.py`, `fz/logging.py`, `fz/shell.py` | Configuration (`FZ_*`), logs, bash / `FZ_SHELL_PATH` resolution |

Documentation lives in three places that must stay consistent when the API or the CLI
changes: `README.md`, `doc/`, and the agent skill `skills/fz/` (tested by
`tests/test_skill_static.py`). This website is a separate repository,
[Funz/fz.github.io](https://github.com/Funz/fz.github.io).

## Workflow

1. Fork and branch from `main`.
2. Add or update tests under `tests/` for any behaviour change.
3. Run the suite (see [Testing](testing.md)) — keep it green on Linux, macOS, and
   Windows where feasible.
4. Update `NEWS.md` under `## Unreleased`.
5. Open a pull request.

## Releasing

`fz/_version.py` is stamped by CI (`scripts/stamp_version.py`) and must not be edited by
hand; `pyproject.toml` reads the version dynamically. A release commit folds `## Unreleased` into a dated `## Version X.Y` section in
`NEWS.md`, and aligns the Claude Code plugin version. Publishing a GitHub Release with
the matching tag triggers `release.yml`, which pushes to PyPI.

## See Also

- [Testing](testing.md)
- [Writing Algorithms](../user-guide/design/algorithms.md)
- [Plugin templates](../plugins/index.md#creating-your-own-plugin) — `fz-Model`, `fz-Algorithm`, `fz-AlgorithmR`
