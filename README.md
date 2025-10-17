# FZ Documentation Website

This repository hosts the documentation website for [FZ - Parametric Scientific Computing Framework](https://github.com/Funz/fz).

## 📚 Documentation Site

Visit the live documentation at: **https://funz.github.io/fz**

## 🚀 Quick Links

- [Installation Guide](https://funz.github.io/fz/getting-started/installation/)
- [Quick Start](https://funz.github.io/fz/getting-started/quickstart/)
- [Core Functions](https://funz.github.io/fz/user-guide/core-functions/fzr/)
- [Plugins](https://funz.github.io/fz/plugins/)
- [Google Colab Notebooks](https://funz.github.io/fz/examples/colab/)

## 📓 Google Colab Examples

Try FZ directly in your browser:

- [Perfect Gas Example](https://colab.research.google.com/github/Funz/fz.github.io/blob/main/notebooks/perfectgas_example.ipynb)
- [OpenModelica Integration](https://colab.research.google.com/github/Funz/fz.github.io/blob/main/notebooks/modelica_example.ipynb)

## 🔌 FZ Plugins

- [FZ-Moret](https://github.com/Funz/fz-moret) - Moret model plugin
- [FZ-MCNP](https://github.com/Funz/fz-mcnp) - Monte Carlo N-Particle Transport
- [FZ-Cathare](https://github.com/Funz/fz-cathare) - Thermal-hydraulic system code
- [FZ-Cristal](https://github.com/Funz/fz-cristal) - Cristal simulation plugin
- [FZ-Scale](https://github.com/Funz/fz-scale) - Scale nuclear analysis code
- [FZ-Telemac](https://github.com/Funz/fz-telemac) - Hydrodynamics simulation system

## 🛠️ Building the Documentation

This site is built with [MkDocs](https://www.mkdocs.org/) and the [Material theme](https://squidfunk.github.io/mkdocs-material/).

### Prerequisites

```bash
pip install mkdocs mkdocs-material pymdown-extensions
```

### Local Development

```bash
# Clone the repository
git clone https://github.com/Funz/fz.github.io.git
cd fz.github.io

# Serve locally with live reload
mkdocs serve

# Open http://127.0.0.1:8000 in your browser
```

### Build

```bash
# Build static site
mkdocs build

# Output in site/ directory
```

### Deploy

The documentation is automatically deployed to GitHub Pages when changes are pushed to the `main` branch via GitHub Actions.

## 📝 Contributing

Contributions to the documentation are welcome! Please:

1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Test locally with `mkdocs serve`
5. Submit a pull request

### Adding Content

- Documentation pages are in `docs/`
- Notebooks are in `notebooks/`
- Configuration is in `mkdocs.yml`

## 📄 License

BSD 3-Clause License - see the [FZ repository](https://github.com/Funz/fz) for details.