# Installation

FZ is a Python package that requires Python 3.8 or later. This guide covers different installation methods and optional dependencies.

## Requirements

- **Python**: 3.8 or later
- **Operating System**: Linux, macOS, or Windows
- **Optional**: SSH access for remote calculators, pandas for DataFrame output

## Installation Methods

### From Source (Recommended)

Install the latest development version from GitHub:

```bash
git clone https://github.com/Funz/fz.git
cd fz
pip install -e .
```

The `-e` flag installs in editable mode, which is useful for development.

### From PyPI (Coming Soon)

Once published to PyPI, you'll be able to install with:

```bash
pip install funz
```

### Using Virtual Environment (Recommended)

It's best practice to use a virtual environment:

```bash
# Create virtual environment
python -m venv fz-env

# Activate it
# On Linux/macOS:
source fz-env/bin/activate
# On Windows:
fz-env\Scripts\activate

# Install FZ
pip install -e /path/to/fz
```

## Optional Dependencies

FZ has several optional dependencies for additional features:

### SSH Support

For remote calculator execution via SSH:

```bash
pip install paramiko
```

### DataFrame Support

For pandas DataFrame output (highly recommended):

```bash
pip install pandas
```

### All Optional Dependencies

Install everything at once:

```bash
pip install paramiko pandas
```

## Verify Installation

Test that FZ is properly installed:

```bash
python -c "import fz; print('FZ version:', fz.__version__)"
```

You should see output like:
```
FZ version: 0.9.0
```

## Google Colab

To use FZ in Google Colab, add this to your notebook:

```python
!pip install git+https://github.com/Funz/fz.git
```

Or for a specific version:

```python
!pip install git+https://github.com/Funz/fz.git@v0.9.0
```

## Installing Plugins

FZ plugins are separate packages. Install them as needed:

### FZ-Moret

```bash
git clone https://github.com/Funz/fz-moret.git
cd fz-moret
pip install -e .
```

### FZ-MCNP

```bash
git clone https://github.com/Funz/fz-mcnp.git
cd fz-mcnp
pip install -e .
```

### Other Plugins

Follow the same pattern for other plugins:

- [FZ-Cathare](https://github.com/Funz/fz-cathare)
- [FZ-Cristal](https://github.com/Funz/fz-cristal)
- [FZ-Scale](https://github.com/Funz/fz-scale)
- [FZ-Telemac](https://github.com/Funz/fz-telemac)

## Development Installation

For FZ development, install additional dependencies:

```bash
# Clone the repository
git clone https://github.com/Funz/fz.git
cd fz

# Install with development dependencies
pip install -e ".[dev]"

# Run tests to verify
pytest tests/
```

## Troubleshooting

### Import Error

If you get `ModuleNotFoundError: No module named 'fz'`:

1. Verify installation: `pip list | grep fz`
2. Check your Python path: `python -c "import sys; print(sys.path)"`
3. Ensure you're using the correct Python environment

### SSH Connection Issues

If SSH calculators fail:

1. Install paramiko: `pip install paramiko`
2. Test SSH manually: `ssh user@host`
3. Check host keys are accepted
4. Verify network connectivity

### Permission Errors

On Linux/macOS, if you get permission errors:

```bash
# Use --user flag
pip install --user -e .

# Or use sudo (not recommended)
sudo pip install -e .
```

## System-Specific Notes

### Windows

- Use PowerShell or Command Prompt
- Some shell calculators may require WSL or Git Bash
- Path separators are backslashes (`\`) instead of forward slashes (`/`)

### macOS

- May need Xcode Command Line Tools: `xcode-select --install`
- Use Homebrew to install Python if needed: `brew install python`

### Linux

- Use your distribution's package manager for Python:
    - Ubuntu/Debian: `sudo apt install python3 python3-pip`
    - Fedora/RHEL: `sudo dnf install python3 python3-pip`
    - Arch: `sudo pacman -S python python-pip`

## HPC Environments

For HPC clusters, you may need to:

1. Load Python module: `module load python/3.9`
2. Install to user directory: `pip install --user -e .`
3. Add to PATH: `export PATH=$HOME/.local/bin:$PATH`

## Docker Installation (Advanced)

Create a Dockerfile for containerized FZ:

```dockerfile
FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install FZ
RUN pip install git+https://github.com/Funz/fz.git

# Set working directory
WORKDIR /workspace

# Default command
CMD ["python"]
```

Build and run:

```bash
docker build -t fz-env .
docker run -it -v $(pwd):/workspace fz-env
```

## Next Steps

Once installed, proceed to:

- [Quick Start Guide](quickstart.md) - Your first FZ calculation
- [Core Concepts](concepts.md) - Understand FZ fundamentals
- [Examples](../examples/perfectgas.md) - See FZ in action
