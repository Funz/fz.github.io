# Installation

## Requirements

| Item | Requirement |
|------|-------------|
| Python | ≥ 3.9 (CI tests 3.9 to 3.13; 3.14 as pre-release only) |
| Required packages | `paramiko`, `pandas`, `charset-normalizer` (installed automatically) |
| bash | Needed by `sh://` calculators and shell output commands. Native on Linux/macOS; MSYS2 or Git Bash on Windows |
| Operating system | Linux, macOS, Windows |

Optional components, needed only for the matching feature:

| Feature | Install |
|---------|---------|
| R formulas (`interpreter: "R"`) and R algorithms | R + `pip install 'funz-fz[r]'` (rpy2) |
| MCP server `fz-mcp` | `pip install 'funz-fz[mcp]'` — Python ≥ 3.10 only |
| `hdf5_file()` output helper | `pip install h5py` |
| `jq://`, `yq://`, `xpath://` outputs | `jq`, [mikefarah/yq](https://github.com/mikefarah/yq), `xmllint` on `PATH` |
| `slurm://`, `slurm-array://` | SLURM client commands (`srun`; `sbatch`/`sacct` for arrays) |
| `funz://` | A running Java Funz calculator |

## Install

=== "pip"

    ```bash
    pip install funz-fz
    ```

=== "pipx (CLI only)"

    ```bash
    pipx install funz-fz
    ```

=== "virtual environment"

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate      # Windows: .venv\Scripts\activate
    pip install funz-fz
    ```

    Use this form on systems that refuse `pip install` with
    `error: externally-managed-environment` (PEP 668).

=== "from source"

    ```bash
    git clone https://github.com/Funz/fz.git
    cd fz
    pip install -e ".[dev]"        # editable, with test dependencies
    ```

This installs the Python package `fz` and the commands `fz`, `fzi`, `fzc`, `fzo`, `fzr`,
`fzd`, `fzl` (and `fz-mcp` when the `mcp` extra is installed).

## Verify

```bash
fz --version
python -c "import fz; print(fz.__version__)"
fz list --check           # models/calculators found in ./.fz and ~/.fz
```

## Windows

- Install [MSYS2](https://www.msys2.org/) or Git Bash, then point `FZ_SHELL_PATH` at the
  directories containing `bash` and the Unix tools, before starting Python:

    ```powershell
    $env:FZ_SHELL_PATH = "C:\msys64\usr\bin;C:\msys64\mingw64\bin"
    ```

- `import fz` works without bash; only `sh://` calculators and shell output commands need
  it. The `python://`, `jq://`, `yq://` and `xpath://` output forms do not.
- Relative `input_static` files are symlinked into each case; without symlink permission
  (no developer mode/admin) they are copied.
- Write templates with Unix line endings when they are sourced by bash scripts.

## HPC login nodes

```bash
module load python/3.11        # site-specific
python3 -m venv ~/fz-venv && source ~/fz-venv/bin/activate
pip install funz-fz
```

Calculator scripts executed remotely through `ssh://` or `slurm://` do not need fz on the
remote side: fz only needs to be installed where the study is launched.

## Google Colab

```python
!pip install funz-fz
```

See [Google Colab Notebooks](../examples/colab.md).

## Models and algorithms for specific codes

Ready-made wrappers (`fz-<code>` repositories) are installed with fz itself, not with
pip:

```bash
fz install model Moret          # -> https://github.com/Funz/fz-Moret, into ./.fz/
fz install algorithm brent      # -> https://github.com/Funz/fz-brent
```

See [Installing Models & Algorithms](../user-guide/installing.md) and
[Plugins](../plugins/index.md).

## Next steps

- [Quick Start](quickstart.md)
- [Core Concepts](concepts.md)
- [Constraints & Limits](../reference/limitations.md)
