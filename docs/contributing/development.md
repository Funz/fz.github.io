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

Optional extras: `paramiko` (SSH/SLURM), `pandas` (DataFrame output), `rpy2` + R
(R interpreter and R algorithm plugins), `h5py` (HDF5 outputs).

## Package Layout

| Module | Responsibility |
|--------|----------------|
| `fz/core.py` | The public functions `fzi`, `fzc`, `fzo`, `fzr`, `fzd` |
| `fz/interpreter.py` | Variable parsing, formula evaluation (Python / R) |
| `fz/runners.py` | Calculator backends — `sh://`, `ssh://`, `slurm://`, `funz://`, `cache://` |
| `fz/helpers.py` | Parallel scheduling, retry, interrupt handling |
| `fz/io.py` | File staging, hashing, `.fz_hash` caching |
| `fz/algorithms.py` | Algorithm framework for `fzd` |
| `fz/shell.py` | Shell utilities, `FZ_SHELL_PATH` binary resolution |
| `fz/cli.py` | `fz`, `fzi`, `fzc`, `fzo`, `fzr`, `fzd`, `fzl` entry points |
| `fz/config.py` | Environment-variable configuration |

## Workflow

1. Fork and branch from `main`.
2. Add or update tests under `tests/` for any behaviour change.
3. Run the suite (see [Testing](testing.md)) — keep it green on Linux, macOS, and
   Windows where feasible.
4. Update `NEWS.md` under `## Unreleased`.
5. Open a pull request.

## Releasing

Version lives in `fz/__init__.py` (`pyproject.toml` reads it dynamically). A release
commit bumps that, folds `## Unreleased` into a dated `## Version X.Y` section in
`NEWS.md`, and aligns the Claude Code plugin version. Publishing a GitHub Release with
the matching tag triggers `release.yml`, which pushes to PyPI.

## See Also

- [Testing](testing.md)
- [Writing Custom Algorithms](../user-guide/core-functions/fzd.md#writing-custom-algorithms)
- [Plugin templates](../plugins/index.md#creating-your-own-plugin) — `fz-Model`, `fz-Algorithm`, `fz-AlgorithmR`
